from fastapi import FastAPI 
from database import db_conn
from auth import router as auth_router
from routes.articles import router as articles_router
from routes.admin import router as admin_router

app = FastAPI()

#initializing the database
db_conn()

#attaching the routers
app.include_router(auth_router)
app.include_router(articles_router)
app.include_router(admin_router,prefix="/admin")

