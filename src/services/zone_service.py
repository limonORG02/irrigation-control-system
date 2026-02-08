from database.db import get_connection

def get_zones():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, plant_type FROM zones")
    zones = cur.fetchall()
    conn.close()
    return zones
