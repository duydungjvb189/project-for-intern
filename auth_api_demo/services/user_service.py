from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user_model import User
from utils.jwt_handler import decode_token

def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.id

def get_all_users_service(db: Session):
    users = db.query(User).all()
    return users