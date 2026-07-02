from pydantic import BaseModel, Field
import datetime

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
