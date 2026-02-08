from database.models import init_db
from services.zone_service import get_zones
from services.sensor_service import get_sensors_by_zone
from services.irrigation_service import get_norms
from analysis.decision_engine import analyze_zone
from utils.logger import log

def main():
    init_db()
    zones = get_zones()

    for zone_id, _name, plant_type in zones:
        sensors_data = get_sensors_by_zone(zone_id)
        norms = get_norms(plant_type)

        if not norms:
            log(f"Нет нормативов для {plant_type}", "ERROR")
            continue

        status = analyze_zone(zone_id, plant_type, sensors_data, norms)
        log(f"Зона {zone_id}: {status}")

if __name__ == "__main__":
    main()
