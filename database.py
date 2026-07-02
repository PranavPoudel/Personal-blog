import sqlite3
import datetime

def db_conn():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, published_date TEXT, visits INTEGER DEFAULT 0)")
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect("blog.db")
    return conn

def now():
    return datetime.datetime.now().isoformat()