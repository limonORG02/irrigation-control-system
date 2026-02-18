from database.db import get_connection
from database.models import init_db


def init_demo_data():
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    # Зоны
    cur.execute("INSERT OR IGNORE INTO zones VALUES (1, 'Газон 10x10', 100, 'lawn')")
    cur.execute("INSERT OR IGNORE INTO zones VALUES (2, 'Клумба', 25, 'flowers')")
    cur.execute("INSERT OR IGNORE INTO zones VALUES (3, 'Аллея', 40, 'trees')")

    # Датчики влажности
    cur.execute(
        "INSERT OR IGNORE INTO sensors (id, zone_id, sensor_type, location_note) VALUES (1, 1, 'moisture', 'центр зоны')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO sensors (id, zone_id, sensor_type, location_note) VALUES (2, 1, 'moisture', 'край зоны')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO sensors (id, zone_id, sensor_type, location_note) VALUES (3, 2, 'moisture', 'вход в клумбу')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO sensors (id, zone_id, sensor_type, location_note) VALUES (4, 2, 'moisture', 'центр клумбы')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO sensors (id, zone_id, sensor_type, location_note) VALUES (5, 3, 'moisture', 'аллея север')"
    )

    # Газовые датчики стоят только на части территории
    cur.execute(
        "INSERT OR IGNORE INTO sensors (id, zone_id, sensor_type, location_note) VALUES (6, 1, 'gas', 'у техпомещения')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO sensors (id, zone_id, sensor_type, location_note) VALUES (7, 3, 'gas', 'рядом с парковкой')"
    )

    # Нормативы влажности
    cur.execute("INSERT OR IGNORE INTO norms VALUES ('lawn', 20, 30)")
    cur.execute("INSERT OR IGNORE INTO norms VALUES ('flowers', 25, 40)")
    cur.execute("INSERT OR IGNORE INTO norms VALUES ('trees', 30, 50)")

    # Измерения влажности
    moisture_measurements = [
        (1, 18),
        (2, 22),
        (3, 35),
        (4, 38),
        (5, 33),
    ]

    for sensor_id, moisture in moisture_measurements:
        cur.execute(
            """
            INSERT INTO measurements (sensor_id, moisture, gas_ppm)
            VALUES (?, ?, NULL)
        """,
            (sensor_id, moisture),
        )

    # Измерения газа (ppm)
    gas_measurements = [
        (6, 640),  # предупреждение для зоны 1
        (7, 420),  # норма для зоны 3
    ]

    for sensor_id, gas_ppm in gas_measurements:
        cur.execute(
            """
            INSERT INTO measurements (sensor_id, moisture, gas_ppm)
            VALUES (?, NULL, ?)
        """,
            (sensor_id, gas_ppm),
        )

    conn.commit()
    conn.close()

    print("Демо-данные успешно созданы")


if __name__ == "__main__":
    init_demo_data()
