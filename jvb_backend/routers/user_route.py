from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from models.user_model import User
from services.user_service import get_user_by_id, get_all_users_service, get_user_status
from schemas.user_schemas import UserResponse
from utils.jwt_handler import decode_token

router = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    return get_user_by_id(db, payload["sub"])

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return UserResponse.from_orm(current_user)

@router.get("/all", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return get_all_users_service(db)

@router.get("/status/{user_id}")
def check_user_status(user_id: int):
    status = get_user_status(user_id)

    if not status:
        raise HTTPException(status_code=404, detail="User not found in system")
    
    return status