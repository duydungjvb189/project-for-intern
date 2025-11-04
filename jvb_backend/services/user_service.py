"""User service helpers.

Provides higher-level user-related utilities used by routers and other
service layers. This module contains convenience functions for fetching
users, checking presence information in Redis, and computing offline
durations.
"""

from fastapi import HTTPException
from datetime import datetime
from utils.config import redis_client
from repositories.user_repository import UserRepository


def get_user_by_id(db, user_id: int):
    """Retrieve a single user by their primary key id.

    Args:
        db: SQLAlchemy Session used for lookup.
        user_id: Primary key id of the user to retrieve.

    Returns:
        The User instance when found.

    Raises:
        HTTPException: 404 if the user is not found.
    """
    user_repo = UserRepository(db)

    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_all_users_service(db):
    """Return a list of all users.

    Args:
        db: SQLAlchemy Session used for lookup.

    Returns:
        List of User instances.
    """
    user_repo = UserRepository(db)

    users = user_repo.get_all_users()
    return users


def get_offline_duration(user_id: int):
    """Calculate how long a user has been offline.

    Reads the `user:{user_id}:offline_since` key from Redis (expected to
    be a timestamp) and returns a human-friendly string describing how
    long ago the user went offline.

    Args:
        user_id: ID of the user to check.

    Returns:
        A string like "<n> phút trước" (minutes ago) or None when no
        offline timestamp is available.
    """
    offline_since = redis_client.get(f"user:{user_id}:offline_since")

    if not offline_since:
        return None

    # Redis returns bytes for stored values; ensure we convert to float
    # regardless of the stored representation.
    offline_since = float(offline_since)
    diff = datetime.utcnow().timestamp() - offline_since

    minutes = int(diff // 60)

    # Keep the existing Vietnamese phrasing used in the project
    return f"{minutes} phút trước"


def get_user_status(user_id: int):
    """Return presence information for a user.

    Queries Redis for `user:{user_id}:is_online`. If the value indicates
    the user is online, returns a short dict with `is_online: True`.
    Otherwise, it computes the offline duration and returns that value.

    Args:
        user_id: ID of the user whose status is requested.

    Returns:
        Dict with keys: `user_id`, `is_online` (bool), and
        `offline_duration` (string or None).
    """
    status = redis_client.get(f"user:{user_id}:is_online")

    # Redis may return bytes which should be decoded to string for
    # comparison (or None if key does not exist).
    if isinstance(status, bytes):
        status = status.decode()

    if status == "1":
        return {
            "user_id": user_id,
            "is_online": True,
            "offline_duration": None,
        }

    offline_duration = get_offline_duration(user_id)
    return {
        "user_id": user_id,
        "is_online": False,
        "offline_duration": offline_duration,
    }