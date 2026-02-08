from database.db import get_connection

def get_norms(plant_type):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT min_moisture, max_moisture
        FROM norms WHERE plant_type = ?
    """, (plant_type,))
    result = cur.fetchone()
    conn.close()
    return result
