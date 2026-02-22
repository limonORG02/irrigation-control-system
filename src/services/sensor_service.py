from database.db import get_connection

def get_sensors_by_zone(zone_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT moisture FROM measurements
        JOIN sensors ON sensors.id = measurements.sensor_id
        WHERE sensors.zone_id = ?
    """, (zone_id,))
    data = cur.fetchall()
    conn.close()
    return [row[0] for row in data]

def list_sensors(zone_id=None):
    conn = get_connection()
    cur = conn.cursor()
    if zone_id is None:
        cur.execute("SELECT id, zone_id, type, active FROM sensors")
    else:
        cur.execute("SELECT id, zone_id, type, active FROM sensors WHERE zone_id = ?", (zone_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def add_sensor(zone_id, sensor_type='moisture'):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO sensors (zone_id, type, active) VALUES (?, ?, 1)", (zone_id, sensor_type))
    conn.commit()
    sid = cur.lastrowid
    conn.close()
    return sid

def remove_sensor(sensor_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM sensors WHERE id = ?", (sensor_id,))
    cur.execute("DELETE FROM measurements WHERE sensor_id = ?", (sensor_id,))
    conn.commit()
    conn.close()

def add_measurement(sensor_id, moisture):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO measurements (sensor_id, moisture) VALUES (?, ?)", (sensor_id, moisture))
    conn.commit()
    conn.close()
