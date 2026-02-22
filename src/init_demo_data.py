from database.db import get_connection
from database.models import init_db

def init_demo_data():
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    # Зоны
    cur.execute("INSERT OR IGNORE INTO zones VALUES (1, 'Газон 10x10', 100, 'lawn')")
    cur.execute("INSERT OR IGNORE INTO zones VALUES (2, 'Клумба', 25, 'flowers')")

    # Датчики
    cur.execute("INSERT OR IGNORE INTO sensors (id, zone_id, type, active) VALUES (1, 1, 'moisture', 1)")
    cur.execute("INSERT OR IGNORE INTO sensors (id, zone_id, type, active) VALUES (2, 1, 'moisture', 1)")
    cur.execute("INSERT OR IGNORE INTO sensors (id, zone_id, type, active) VALUES (3, 2, 'moisture', 1)")
    cur.execute("INSERT OR IGNORE INTO sensors (id, zone_id, type, active) VALUES (4, 2, 'moisture', 1)")

    # Нормативы влажности
    cur.execute("""
        INSERT OR IGNORE INTO norms VALUES ('lawn', 20, 30)
    """)
    cur.execute("""
        INSERT OR IGNORE INTO norms VALUES ('flowers', 25, 40)
    """)
    cur.execute("""
        INSERT OR IGNORE INTO norms VALUES ('trees', 30, 50)
    """)

    # Измерения (в процентах влажности)
    measurements = [
        (1, 18),
        (2, 22),
        (3, 35),
        (4, 38)
    ]

    for sensor_id, moisture in measurements:
        cur.execute("""
            INSERT INTO measurements (sensor_id, moisture)
            VALUES (?, ?)
        """, (sensor_id, moisture))

    conn.commit()
    conn.close()

    print("Демо-данные успешно созданы")

if __name__ == "__main__":
    init_demo_data()
