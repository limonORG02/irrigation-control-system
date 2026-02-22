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
        type TEXT DEFAULT 'moisture',
        active INTEGER DEFAULT 1,
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

    # Table for gas/alarm events
    cur.execute("""
    CREATE TABLE IF NOT EXISTS gas_events (
        id INTEGER PRIMARY KEY,
        zone_id INTEGER,
        level REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        acknowledged INTEGER DEFAULT 0,
        FOREIGN KEY(zone_id) REFERENCES zones(id)
    )
    """)

    # Ensure newer columns exist if DB was created with older schema
    try:
        cur.execute("ALTER TABLE sensors ADD COLUMN type TEXT DEFAULT 'moisture'")
    except Exception:
        pass
    try:
        cur.execute("ALTER TABLE sensors ADD COLUMN active INTEGER DEFAULT 1")
    except Exception:
        pass

    conn.commit()
    conn.close()
