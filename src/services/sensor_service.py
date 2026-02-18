from database.db import get_connection


GAS_WARNING_THRESHOLD_PPM = 600
GAS_CRITICAL_THRESHOLD_PPM = 900


def add_sensor(zone_id, sensor_type="moisture", location_note=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO sensors (zone_id, sensor_type, location_note)
        VALUES (?, ?, ?)
    """,
        (zone_id, sensor_type, location_note),
    )
    sensor_id = cur.lastrowid
    conn.commit()
    conn.close()
    return sensor_id


def remove_sensor(sensor_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM measurements WHERE sensor_id = ?", (sensor_id,))
    cur.execute("DELETE FROM sensors WHERE id = ?", (sensor_id,))
    removed = cur.rowcount > 0
    conn.commit()
    conn.close()
    return removed


def get_sensors_by_zone(zone_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT moisture FROM measurements
        JOIN sensors ON sensors.id = measurements.sensor_id
        WHERE sensors.zone_id = ? AND sensors.sensor_type = 'moisture'
    """,
        (zone_id,),
    )
    data = cur.fetchall()
    conn.close()
    return [row[0] for row in data if row[0] is not None]


def get_gas_readings_by_zone(zone_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT gas_ppm FROM measurements
        JOIN sensors ON sensors.id = measurements.sensor_id
        WHERE sensors.zone_id = ? AND sensors.sensor_type = 'gas'
    """,
        (zone_id,),
    )
    data = cur.fetchall()
    conn.close()
    return [row[0] for row in data if row[0] is not None]


def add_measurement(sensor_id, moisture=None, gas_ppm=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO measurements (sensor_id, moisture, gas_ppm)
        VALUES (?, ?, ?)
    """,
        (sensor_id, moisture, gas_ppm),
    )
    conn.commit()
    conn.close()
