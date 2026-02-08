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
