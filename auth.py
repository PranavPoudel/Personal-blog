
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader
from models import userTemplate

router = APIRouter(tags=["Authentication"])

api_key_header = APIKeyHeader(name="admin_token", auto_error= False)

async def verify_token(admin_token : str = Depends(api_key_header)):
    if admin_token != "secret_token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return admin_token

@router.post ("/login")
def login(user:userTemplate):
    if user.username == "Admin" and user.password == "password":
        return "secret_token"
    
