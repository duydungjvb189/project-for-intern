from fastapi import HTTPException
from datetime import datetime
from utils.config import redis_client
from repositories.user_repository import UserRepository

# Retrieve a single user by their ID.
def get_user_by_id(db, user_id: int):
    user_repo = UserRepository(db)

    # Lấy user theo username
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Retrieve all users from the database.
def get_all_users_service(db):
    user_repo = UserRepository(db)

    # Lấy user theo username
    users = user_repo.get_all_users()
    return users

# Calculate how long a user has been offline based on Redis data.
def get_offline_duration(user_id: int):
    offline_since = redis_client.get(f"user:{user_id}:offline_since")

    if not offline_since:
        return None
    
    offline_since = float(offline_since)
    diff = datetime.utcnow().timestamp() - offline_since

    minutes = int(diff // 60)

    return f"{minutes} phút trước"

# Get the current online/offline status of a user from Redis.
def get_user_status(user_id: int):
    status = redis_client.get(f"user:{user_id}:is_online")

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