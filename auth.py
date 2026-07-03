
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader
from models import userTemplate
from config import settings

router = APIRouter(tags=["Authentication"])

api_key_header = APIKeyHeader(name="admin_token", auto_error= False)

async def verify_token(admin_token : str = Depends(api_key_header)):
    if admin_token != settings.secret_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return admin_token

@router.post ("/login")
def login(user:userTemplate):
    if user.username == settings.admin_username and user.password == settings.admin_password:
        return settings.secret_token
    
