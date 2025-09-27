# db_utils.py
import sqlite3, os
DB = os.getenv("DB_PATH", "mercado.db")

def get_conn():
    conn = sqlite3.connect(DB, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn(); cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS produtos (
        ml_id TEXT PRIMARY KEY,
        title TEXT,
        price REAL,
        seller_id TEXT,
        thumbnail TEXT,
        link TEXT,
        status TEXT,
        last_updated TEXT
    );
    """)
    conn.commit(); conn.close()

