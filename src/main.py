from analysis.decision_engine import analyze_zone
from database.models import init_db
from services.irrigation_service import get_norms
from services.sensor_service import get_gas_readings_by_zone, get_sensors_by_zone
from services.zone_service import get_zones
from utils.logger import log


def main():
    init_db()
    zones = get_zones()

    for zone_id, _name, plant_type in zones:
        moisture_data = get_sensors_by_zone(zone_id)
        gas_data = get_gas_readings_by_zone(zone_id)
        norms = get_norms(plant_type)

        if not norms:
            log(f"Нет нормативов для {plant_type}", "ERROR")
            continue

        result = analyze_zone(zone_id, plant_type, moisture_data, norms, gas_data)
        log(
            f"Зона {zone_id}: {result['status']} (влажность: {result['moisture_status']}, газ: {result['gas_status']})"
        )


if __name__ == "__main__":
    main()
