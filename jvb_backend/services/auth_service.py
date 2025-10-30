from datetime import datetime
from fastapi import HTTPException, status
from repositories.user_repository import UserRepository
from schemas.user_schemas import UserCreate, UserLogin
from datetime import datetime
from utils.config import redis_client
from utils.jwt_handler import create_access_token, create_refresh_token
from utils.password_hash import hash_password, verify_password

def register_user_service(db, user_data: UserCreate):
    user_repo = UserRepository(db)

    if user_repo.get_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if user_repo.get_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    hashed_password = hash_password(user_data.password)
    
    user_repo.create_user(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )

    return { "message": "User registered successfully" }

def login_user_service(user_data: UserLogin, db):
    user_repo = UserRepository(db)

    # Lấy user theo username
    user = user_repo.get_by_username(user_data.username)

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    access_token = create_access_token(user.id, user.username)
    refresh_token = create_refresh_token(user.id, user.username)

    # Nếu đăng nhập thành công sẽ bắt đầu lưu trạng thái online
    now = datetime.utcnow().timestamp()

    # Đánh dấu online
    redis_client.set(f"user:{user.id}:is_online", 1)
    redis_client.set(f"user:{user.id}:last_login", now)
    
    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_status": {
            "is_online": True,
            "last_login": datetime.utcfromtimestamp(now).isoformat(),
        }
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

def logout_user_service(token: int, exp: int, user_id: int):
    ttl = exp - int(datetime.utcnow().timestamp())
    
    if ttl < 0:
        ttl = 0
    
    redis_client.setex(f"blacklist:{token}", ttl, "revoked")

    # Đánh dấu offline
    now = datetime.utcnow().timestamp()
    redis_client.set(f"user:{user_id}:is_online", 0)
    redis_client.set(f"user:{user_id}:offline_since", now)

    return {
        "message": "User logged out successfully",
        "user_status": {
            "is_online": False,
            "offline_since": datetime.utcfromtimestamp(now).isoformat()
        }
    }