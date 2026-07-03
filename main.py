from contextlib import asynccontextmanager
from fastapi import FastAPI 
from database import db_conn
from auth import router as auth_router
from routes.articles import router as articles_router
from routes.admin import router as admin_router



@asynccontextmanager
async def lifespan(app:FastAPI):
    #this will run exactly once when the server starts
    db_conn()
    yield
    #will run once when server stops, here is where we will close resources, (for sqlite, leaving empty is fine)

app = FastAPI(lifespan= lifespan)


#attaching the routers
app.include_router(auth_router)
app.include_router(articles_router)
app.include_router(admin_router,prefix="/admin")

