from fastapi import HTTPException
from datetime import datetime
from utils.config import redis_client
from repositories.user_repository import UserRepository

def get_user_by_id(db, user_id: int):
    user_repo = UserRepository(db)

    # Lấy user theo username
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_all_users_service(db):
    user_repo = UserRepository(db)

    # Lấy user theo username
    users = user_repo.get_all_users()
    return users

def get_offline_duration(user_id: int):
    offline_since = redis_client.get(f"user:{user_id}:offline_since")

    if not offline_since:
        return None
    
    offline_since = float(offline_since)
    diff = datetime.utcnow().timestamp() - offline_since

    minutes = int(diff // 60)

    return f"{minutes} phút trước"

def get_user_status(user_id: int):
    status = redis_client.get(f"user:{user_id}:is_online")

    # Nếu redis trả về bytes thì decode, còn nếu là str thì giữ nguyên
    if isinstance(status, bytes):
        status = status.decode()

    if status == "1":
        return {
            "user_id": user_id,
            "is_online": True,
            "offline_duration": None
        }

    offline_duration = get_offline_duration(user_id)
    return {
        "user_id": user_id,
        "is_online": False,
        "offline_duration": offline_duration
    }