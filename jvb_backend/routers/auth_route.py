from fastapi import APIRouter, Depends
from fastapi import Body
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models.user_model import User
from services.auth_service import (
    register_user_service,
    login_user_service,
    refresh_token_service,
    logout_user_service
)
from services.user_service import get_user_by_id
from schemas.user_schemas import UserCreate, UserLogin
from schemas.token_schemas import TokenData, RefreshTokenData, RefreshTokenRequest
from utils.jwt_handler import decode_token

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    return get_user_by_id(db, payload["sub"])

@router.post("/register", response_model=dict)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return register_user_service(db, user_data)

@router.post("/login", response_model=TokenData)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    return login_user_service(user_data, db)

@router.post("/token/refresh", response_model=RefreshTokenData)
def refresh_token(data: RefreshTokenRequest):
    token = data.refresh_token
    
    return refresh_token_service(token)

@router.post("/logout", response_model=dict)
def logout_user(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    exp = payload.get("exp")

    return logout_user_service(token, exp, current_user.id)