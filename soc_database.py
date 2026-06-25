import sqlite3
from datetime import datetime


DATABASE = "soc_events.db"


def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        category TEXT,

        threat_level TEXT,

        threat_score INTEGER,

        file_hash TEXT,

        action TEXT,

        timestamp TEXT

    )
    """)

    conn.commit()
    conn.close()



def add_event(filename, category, level, score, file_hash, action):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute("""
    INSERT INTO events
    (
    filename,
    category,
    threat_level,
    threat_score,
    file_hash,
    action,
    timestamp
    )

    VALUES (?,?,?,?,?,?,?)
    """,

    (
    filename,
    category,
    level,
    score,
    file_hash,
    action,
    str(datetime.now())
    ))


    conn.commit()
    conn.close()



def show_events():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM events ORDER BY id DESC"
    )


    rows = cursor.fetchall()


    for row in rows:
        print(row)


    conn.close()



if __name__ == "__main__":

    create_database()

    print("[+] SOC Database Ready")
