import sqlite3

DB_NAME = "google_repos.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS repositories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repo_name TEXT UNIQUE,
            language TEXT,
            stars INTEGER
        )
    """)
    conn.commit()
    conn.close()


def save_repos(data):
    """data = list of (repo_name, language, stars) tuples"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.executemany(
        "INSERT OR REPLACE INTO repositories (repo_name, language, stars) VALUES (?, ?, ?)",
        data,
    )
    conn.commit()
    conn.close()