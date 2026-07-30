import sqlite3

DB_NAME = "bot.db"


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pairs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source INTEGER,
        destination INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    cur.execute(
        "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
        ("forwarding", "on")
    )

    conn.commit()
    conn.close()


def add_pair(source, destination):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO pairs(source, destination) VALUES(?, ?)",
        (source, destination)
    )

    conn.commit()
    conn.close()


def remove_pair(pair_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM pairs WHERE id=?",
        (pair_id,)
    )

    conn.commit()
    conn.close()


def get_pairs():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, source, destination FROM pairs"
    )

    rows = cur.fetchall()

    conn.close()

    return rows


def forwarding_enabled():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT value FROM settings WHERE key='forwarding'"
    )

    value = cur.fetchone()[0]

    conn.close()

    return value == "on"


def set_forwarding(status):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE settings SET value=? WHERE key='forwarding'",
        (status,)
    )

    conn.commit()
    conn.close()
