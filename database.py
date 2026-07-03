import sqlite3
import datetime
from config import settings

def db_conn():
    conn = sqlite3.connect(settings.database_url)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, published_date TEXT, visits INTEGER DEFAULT 0)")
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(settings.database_url)
    try:
        yield conn
    finally:
        conn.close()


def now():
    return datetime.datetime.now().isoformat()