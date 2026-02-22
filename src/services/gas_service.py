from database.db import get_connection

def record_gas_event(zone_id, level):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO gas_events (zone_id, level, acknowledged) VALUES (?, ?, 0)", (zone_id, level))
    conn.commit()
    eid = cur.lastrowid
    conn.close()
    return eid

def list_unacknowledged():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, zone_id, level, timestamp FROM gas_events WHERE acknowledged = 0 ORDER BY timestamp DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def acknowledge(event_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE gas_events SET acknowledged = 1 WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

def list_events(zone_id=None, acknowledged=None):
    """List gas events with optional filters.

    acknowledged: None (all), 0 (unacknowledged), 1 (acknowledged)
    """
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT id, zone_id, level, timestamp, acknowledged FROM gas_events"
    params = []
    clauses = []
    if zone_id is not None:
        clauses.append("zone_id = ?")
        params.append(zone_id)
    if acknowledged is not None:
        clauses.append("acknowledged = ?")
        params.append(acknowledged)
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY timestamp DESC"
    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    conn.close()
    return rows
