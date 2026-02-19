from analysis.decision_engine import analyze_zone
from database.db import get_connection
from services.irrigation_service import get_norms
from services.sensor_service import get_gas_readings_by_zone, get_sensors_by_zone


def get_zones():
    """Return zones list as tuples: (id, name, plant_type)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, plant_type FROM zones")
    zones = cur.fetchall()
    conn.close()
    return zones


def _has_gas_sensor(zone_id):
    """Check if zone has at least one active gas sensor."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT 1
        FROM sensors
        WHERE zone_id = ? AND sensor_type = 'gas'
        LIMIT 1
    """,
        (zone_id,),
    )
    exists = cur.fetchone() is not None
    conn.close()
    return exists


def get_gas_history(zone_id):
    """Return gas history points and zone metadata for chart rendering."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM zones WHERE id = ?", (zone_id,))
    zone = cur.fetchone()

    cur.execute(
        """
        SELECT measurements.timestamp, measurements.gas_ppm
        FROM measurements
        JOIN sensors ON sensors.id = measurements.sensor_id
        WHERE sensors.zone_id = ?
          AND sensors.sensor_type = 'gas'
          AND measurements.gas_ppm IS NOT NULL
        ORDER BY measurements.timestamp ASC, measurements.id ASC
    """,
        (zone_id,),
    )
    rows = cur.fetchall()
    conn.close()

    return {
        "zone_id": zone_id,
        "zone_name": zone[0] if zone else None,
        "labels": [row[0] for row in rows],
        "values": [row[1] for row in rows],
    }


def get_zone_summaries():
    """Build per-zone summary including moisture, gas and combined status."""
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
                "has_gas_sensor": _has_gas_sensor(zone_id),
            }
        )

    return summaries
