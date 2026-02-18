from analysis.decision_engine import analyze_zone
from database.db import get_connection
from services.irrigation_service import get_norms
from services.sensor_service import get_gas_readings_by_zone, get_sensors_by_zone


def get_zones():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, plant_type FROM zones")
    zones = cur.fetchall()
    conn.close()
    return zones


def get_zone_summaries():
    summaries = []
    zones = get_zones()

    for zone_id, name, plant_type in zones:
        moisture_values = get_sensors_by_zone(zone_id)
        avg_moisture = (
            sum(moisture_values) / len(moisture_values) if moisture_values else None
        )

        gas_values = get_gas_readings_by_zone(zone_id)
        peak_gas = max(gas_values) if gas_values else None

        norms = get_norms(plant_type)
        if not norms:
            analysis_result = {
                "status": "Нет нормативов",
                "moisture_status": "Нет нормативов",
                "gas_status": "Нет нормативов",
            }
        else:
            analysis_result = analyze_zone(
                zone_id,
                plant_type,
                moisture_values,
                norms,
                gas_values,
            )

        summaries.append(
            {
                "id": zone_id,
                "name": name,
                "plant_type": plant_type,
                "avg_moisture": avg_moisture,
                "peak_gas": peak_gas,
                "status": analysis_result["status"],
                "gas_status": analysis_result["gas_status"],
            }
        )

    return summaries
