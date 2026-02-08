from database.db import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS zones (
        id INTEGER PRIMARY KEY,
        name TEXT,
        area REAL,
        plant_type TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sensors (
        id INTEGER PRIMARY KEY,
        zone_id INTEGER,
        FOREIGN KEY(zone_id) REFERENCES zones(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS measurements (
        id INTEGER PRIMARY KEY,
        sensor_id INTEGER,
        moisture REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS norms (
        plant_type TEXT PRIMARY KEY,
        min_moisture REAL,
        max_moisture REAL
    )
    """)

    conn.commit()
    conn.close()
