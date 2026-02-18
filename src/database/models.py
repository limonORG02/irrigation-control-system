from database.db import get_connection


def _column_exists(cur, table_name, column_name):
    cur.execute(f"PRAGMA table_info({table_name})")
    columns = {row[1] for row in cur.fetchall()}
    return column_name in columns


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS zones (
        id INTEGER PRIMARY KEY,
        name TEXT,
        area REAL,
        plant_type TEXT
    )
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS sensors (
        id INTEGER PRIMARY KEY,
        zone_id INTEGER,
        sensor_type TEXT DEFAULT 'moisture',
        location_note TEXT,
        FOREIGN KEY(zone_id) REFERENCES zones(id)
    )
    """
    )

    if not _column_exists(cur, "sensors", "sensor_type"):
        cur.execute("ALTER TABLE sensors ADD COLUMN sensor_type TEXT DEFAULT 'moisture'")

    if not _column_exists(cur, "sensors", "location_note"):
        cur.execute("ALTER TABLE sensors ADD COLUMN location_note TEXT")

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS measurements (
        id INTEGER PRIMARY KEY,
        sensor_id INTEGER,
        moisture REAL,
        gas_ppm REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(sensor_id) REFERENCES sensors(id)
    )
    """
    )

    if not _column_exists(cur, "measurements", "gas_ppm"):
        cur.execute("ALTER TABLE measurements ADD COLUMN gas_ppm REAL")

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS norms (
        plant_type TEXT PRIMARY KEY,
        min_moisture REAL,
        max_moisture REAL
    )
    """
    )

    conn.commit()
    conn.close()
