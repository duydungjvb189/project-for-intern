"""Authentication service helpers.

This module implements higher-level authentication operations used by the
routers and API endpoints. Functions here orchestrate repository access,
password hashing/verification, JWT creation/decoding, and small Redis
side-effects (presence, token blacklisting).

Note: These helpers raise `HTTPException` with appropriate status codes
when validation or authentication fails so that FastAPI routers can
propagate HTTP responses directly.
"""

from datetime import datetime
from fastapi import HTTPException, status
from repositories.user_repository import UserRepository
from schemas.user_schemas import UserCreate, UserLogin
from utils.config import redis_client
from utils.jwt_handler import create_access_token, create_refresh_token
from utils.password_hash import hash_password, verify_password


def register_user_service(db, user_data: UserCreate):
    """Register a new user.

    Validates that the provided email and username are unique, hashes the
    provided plaintext password, and creates a new user record.

    Args:
        db: SQLAlchemy Session used for persistence.
        user_data: `UserCreate` containing username, email, and password.

    Returns:
        A dict containing a success message.

    Raises:
        HTTPException: 400 if email or username is already taken.
    """
    user_repo = UserRepository(db)

    if user_repo.get_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    if user_repo.get_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # Hash the plaintext password before persisting
    hashed_password = hash_password(user_data.password)

    user_repo.create_user(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
    )

    return {"message": "User registered successfully"}


def login_user_service(user_data: UserLogin, db):
    """Authenticate a user and return tokens.

    Verifies the provided credentials, issues access and refresh tokens,
    and records a small presence snapshot in Redis.

    Args:
        user_data: `UserLogin` with username and password.
        db: SQLAlchemy Session for user lookup.

    Returns:
        A dict with message, access_token, refresh_token, token_type, and
        user_status containing presence information.

    Raises:
        HTTPException: 401 when authentication fails.
    """
    user_repo = UserRepository(db)

    user = user_repo.get_by_username(user_data.username)

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Issue tokens
    access_token = create_access_token(user.id, user.username)
    refresh_token = create_refresh_token(user.id, user.username)

    now = datetime.utcnow().timestamp()

    # Update presence info in Redis
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
        },
    }


def refresh_token_service(refresh_token: str):
    """Exchange a refresh token for a new access token.

    Decodes and validates the refresh token payload, then issues a new
    access token for the subject. This function intentionally leaves
    refresh token rotation/persisted revocation to higher-level logic.

    Args:
        refresh_token: The refresh token string presented by the client.

    Returns:
        A dict containing a new access_token and token_type.

    Raises:
        HTTPException: 401 if the token payload is invalid or missing
                        required claims.
    """
    from utils.jwt_handler import decode_refresh_token, create_access_token

    payload = decode_refresh_token(refresh_token)

    user_id = payload.get("sub")
    username = payload.get("username")

    if not user_id or not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload",
        )

    new_access_token = create_access_token(user_id, username)

    return {"access_token": new_access_token, "token_type": "bearer"}


def logout_user_service(token: int, exp: int, user_id: int):
    """Log out a user and revoke the current token.

    Blacklists the provided token in Redis for the remaining TTL and
    marks the user as offline with a timestamp. The function returns a
    small status payload describing the user's new presence state.

    Args:
        token: Token identifier stored in JWT (or a representation used
               as a blacklist key).
        exp: Expiration time (epoch seconds) of the token being revoked.
        user_id: ID of the user to mark as offline.

    Returns:
        A dict containing a confirmation message and the user's new
        presence status.
    """
    ttl = exp - int(datetime.utcnow().timestamp())

    if ttl < 0:
        ttl = 0

    # Store the token in a Redis blacklist for the remaining TTL
    redis_client.setex(f"blacklist:{token}", ttl, "revoked")

    # Mark user offline and record when they went offline
    now = datetime.utcnow().timestamp()
    redis_client.set(f"user:{user_id}:is_online", 0)
    redis_client.set(f"user:{user_id}:offline_since", now)

    return {
        "message": "User logged out successfully",
        "user_status": {
            "is_online": False,
            "offline_since": datetime.utcfromtimestamp(now).isoformat(),
        },
    }