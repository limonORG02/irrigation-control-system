import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("PYTHONPATH", str(Path(__file__).resolve().parents[1] / "src"))

import sys

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from analysis.decision_engine import analyze_zone
from database import models
from services import sensor_service


class IrrigationSystemTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp_dir.name) / "test.db"

        def get_test_connection():
            return sqlite3.connect(self.db_path)

        # Monkey patch connections for imported modules
        import database.db as db_module

        db_module.get_connection = get_test_connection
        models.get_connection = get_test_connection
        sensor_service.get_connection = get_test_connection

        models.init_db()

        conn = get_test_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO zones (id, name, area, plant_type) VALUES (1, 'Тест зона', 10, 'lawn')")
        cur.execute("INSERT INTO norms (plant_type, min_moisture, max_moisture) VALUES ('lawn', 20, 30)")
        conn.commit()
        conn.close()

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_add_and_remove_sensor(self):
        sensor_id = sensor_service.add_sensor(1, "moisture", "центр")
        self.assertIsInstance(sensor_id, int)

        sensor_service.add_measurement(sensor_id, moisture=24)
        moisture_values = sensor_service.get_sensors_by_zone(1)
        self.assertEqual(moisture_values, [24])

        removed = sensor_service.remove_sensor(sensor_id)
        self.assertTrue(removed)
        self.assertEqual(sensor_service.get_sensors_by_zone(1), [])

    def test_gas_warning_logic(self):
        moisture_sensor = sensor_service.add_sensor(1, "moisture")
        gas_sensor = sensor_service.add_sensor(1, "gas")

        sensor_service.add_measurement(moisture_sensor, moisture=25)
        sensor_service.add_measurement(gas_sensor, gas_ppm=700)

        result = analyze_zone(
            zone_id=1,
            plant_type="lawn",
            moisture_values=sensor_service.get_sensors_by_zone(1),
            norms=(20, 30),
            gas_values=sensor_service.get_gas_readings_by_zone(1),
        )

        self.assertEqual(result["moisture_status"], "Норма")
        self.assertEqual(result["gas_status"], "Есть вероятность запаха газа")
        self.assertEqual(result["status"], "Норма + Проверить газ")


if __name__ == "__main__":
    unittest.main()
