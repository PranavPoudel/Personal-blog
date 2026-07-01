from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
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

class ArticleCreate(BaseModel):
    title: str
    content: str
    published_date: str

class ArticleUpdate(BaseModel):
    title: str | None= None
    content: str |None= None
    published_date: str | None= None

app = FastAPI()
db_conn()



@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/articles")
async def all_articles():
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT id,title,content FROM articles"
    cursor.execute(query)
    query_res = cursor.fetchall()
    query_result = []
    for q in query_res:
        value = {
            "id": q[0],
            "title" : q[1],
            "content": q[2]
        }
        query_result.append(value)
    conn.close()
    return query_result
   

@app.post("/articles")
async def create_article(article: ArticleCreate):
    conn = get_db()
    cursor = conn.cursor()
    current_date = now()
    query = "INSERT INTO articles(title, content, published_date) VALUES (?,?,?)"
    cursor.execute(query,(article.title, article.content, current_date ))
    conn.commit()
    conn.close()