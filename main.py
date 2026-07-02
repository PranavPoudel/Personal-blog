from fastapi import FastAPI , HTTPException, Depends
from fastapi.security import APIKeyHeader
import sqlite3
from pydantic import BaseModel, Field
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
api_key_header = APIKeyHeader(name="admin_token", auto_error= False)
async def verify_token(admin_token : str = Depends(api_key_header)):
    if admin_token != "secret_token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return admin_token

class userTemplate(BaseModel):
    username: str
    password: str

class ArticleCreate(BaseModel):
    title: str = Field( min_length= 2)
    content: str = Field( min_length= 10)
    

class ArticleUpdate(BaseModel):
    title: str | None= None 
    content: str |None= None
    published_date : datetime.datetime | None = None

app = FastAPI()
db_conn()



@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/articles")
async def all_articles():
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT id,title,content,published_date FROM articles"
    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"datebase error - {e}")
    query_res = cursor.fetchall()
    query_result = []
    for q in query_res:
        value = {
            "id": q[0],
            "title" : q[1],
            "content": q[2],
            "published_date": q[3]
        }
        query_result.append(value)
    conn.close()
    return query_result
   

@app.post("/articles",status_code=201,response_model=ArticleCreate)
async def create_article(article: ArticleCreate, token:str = Depends(verify_token)):
    conn = get_db()
    cursor = conn.cursor()
    current_date = now()
    query = "INSERT INTO articles(title, content, published_date) VALUES (?,?,?)"
    
    try:
        cursor.execute(query,(article.title, article.content, current_date ))
        conn.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"datebase error - {e}")
    conn.close()
    return {
        "title": article.title,
        "content": article.content
    }

@app.get("/articles/{id}")
async def one_article(id:int):
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT id, title, content, published_date, visits FROM articles WHERE ID = (?)"
    try:
        cursor.execute(query,(id,))
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"datebase error - {e}")
    query_response= cursor.fetchone()

    if query_response is None:
        raise HTTPException(status_code=404, detail="ID doesn't Exists")
    
    query_result = {
        "id": query_response[0],
        "title": query_response[1],
        "content": query_response[2],
        "published_date": query_response[3],
        "visits":query_response[4]
    }
    
    #incrementing the visit for individual aritcles i.e visited article
    visit = query_result["visits"] +1
    query = "UPDATE articles SET visits = (?) WHERE id = (?)"
    cursor.execute(query,(visit, id))
    conn.commit()
    conn.close()
    return query_result


@app.patch ("/articles/{id}", response_model=ArticleUpdate)
async def UpdateOneArticle(id:int,article : ArticleUpdate, token:str=Depends(verify_token)):
    #connecting to database
    conn = get_db()
    cursor = conn.cursor()
    #query to fetch data from database
    query = "SELECT id, title, content, published_date, visits FROM articles WHERE ID = (?)"
    try:
        cursor.execute(query,(id,))
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"datebase error - {e}")
    query_response= cursor.fetchone()

    if query_response is None:
        raise HTTPException(status_code=404, detail="ID doesn't Exists")
    
    query_result = {
        "id": query_response[0],
        "title": query_response[1],
        "content": query_response[2],
        "published_date": query_response[3]
    }
    #setting the new values that are given or maybe not
    if article.title is not None:
        query_result['title'] = article.title
    if article.content is not None:
        query_result['content'] = article.content
    # setting the new dynamic update query
    query = "UPDATE articles SET title = (?), content = (?), published_date = (?) where id = (?)"
    try:
        cursor.execute(query,(query_result['title'],query_result['content'],now(),id))
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"datebase error - {e}")
    conn.commit()
    conn.close()
    return {"message": "Article updated"            
            }

@app.delete ("/articles/{id}", status_code=204)
async def Delete_Articles(id:int, token:str = Depends(verify_token)):
     #connecting to database
    conn = get_db()
    cursor = conn.cursor()
    #query to fetch data from database
    query = "SELECT id FROM articles WHERE ID = (?)"
    try:
        cursor.execute(query,(id,))
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"datebase error - {e}")
    query_response= cursor.fetchone()

    if query_response is None:
        raise HTTPException(status_code=404, detail="ID doesn't Exists")
    
    query = "DELETE FROM articles WHERE id = (?)"
    try:
        cursor.execute(query,(id,))
        conn.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"datebase error - {e}")
    conn.close()
    return 

@app.get ("/admin/dashboard")
async def Admin(token: str = Depends(verify_token)):
    conn = get_db()
    cursor = conn.cursor()

    query ="SELECT * FROM articles"
    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"datebase error - {e}")
    query_response = cursor.fetchall()
    if not query_response:
        raise HTTPException(status_code=404, detail="NO Data in DB")
    
    query_result = []
    for q in query_response:
        value = {
            "id": q[0],
            "title" : q[1],
            "content": q[2],
            "published_date": q[3],
            "visits": q[4]
        }
        query_result.append(value)
    conn.close()
    return query_result

@app.post ("/login")
def login(user:userTemplate):
    if user.username == "Admin" and user.password == "password":
        return "secret_token"
    


