from fastapi import APIRouter, Depends
from fastapi import Body
from sqlalchemy.orm import Session
from database import get_db
from services.auth_service import (
    register_user_service,
    login_user_service,
    refresh_token_service,
    logout_user_service
)
from schemas.user_schemas import UserCreate, UserLogin
from schemas.token_schemas import TokenData, RefreshTokenData, RefreshTokenRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=dict)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return register_user_service(db, user_data)

@router.post("/login", response_model=TokenData)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    return login_user_service(user_data, db)

@router.post("/refresh", response_model=RefreshTokenData)
def refresh_token(data: RefreshTokenRequest):
    token = data.refresh_token
    return refresh_token_service(token)

@router.post("/logout", response_model=dict)
def logout_user():
    return logout_user_service()