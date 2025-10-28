from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user_model import User
from schemas.user_schemas import UserCreate, UserLogin
from utils.jwt_handler import create_access_token, create_refresh_token
from utils.password_hash import hash_password, verify_password

def register_user_service(db: Session, user_data: UserCreate):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    hashed_password = hash_password(user_data.password)
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return { "message": "User registered successfully" }

def login_user_service(user_data: UserLogin, db: Session):
    user = db.query(User).filter(User.username == user_data.username).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    access_token = create_access_token(user.id, user.username)
    refresh_token = create_refresh_token(user.id, user.username)
    
    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def refresh_token_service(refresh_token: str):
    from utils.jwt_handler import decode_refresh_token, create_access_token

    payload = decode_refresh_token(refresh_token)
    
    user_id = payload.get("sub")
    username = payload.get("username")
    
    if not user_id or not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload"
        )

    new_access_token = create_access_token(user_id, username)

    return { "access_token": new_access_token, "token_type": "bearer" }

def logout_user_service():
    return { "message": "User logged out successfully" }