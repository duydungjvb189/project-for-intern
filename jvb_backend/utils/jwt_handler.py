"""JWT helpers

Small utilities to create and validate access/refresh tokens used by the
authentication layer. Tokens are encoded with a project secret and a
configurable algorithm and lifetime. Some functions interact with Redis
to support token blacklisting and presence information.
"""

import os
import datetime
from dotenv import load_dotenv
import time
import jwt
from utils.config import redis_client
from fastapi import HTTPException, status

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))


def create_access_token(user_id: str, username: str) -> str:
    """Create a short-lived JWT access token.

    Args:
        user_id: Identifier of the user (will be placed in the `sub` claim).
        username: Username to include in the token payload.

    Returns:
        Encoded JWT as a string. The token includes `iat` and `exp` claims
        based on `ACCESS_TOKEN_EXPIRE_MINUTES`.
    """
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": int(time.time()) + ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "iat": int(time.time()),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: str, username: str) -> str:
    """Create a long-lived refresh token.

    Args:
        user_id: Identifier of the user.
        username: Username included in the refresh token payload.

    Returns:
        Encoded refresh token string with a longer expiration based on
        `REFRESH_TOKEN_EXPIRE_DAYS`.
    """
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": int(time.time()) + REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        "iat": int(time.time()),
    }

    return jwt.encode(payload, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> str:
    """Decode and validate an access token.

    Performs a Redis blacklist check before decoding. Raises `HTTPException`
    with 401 status for revoked, expired, or invalid tokens so callers can
    return appropriate HTTP responses.

    Args:
        token: Encoded JWT access token.

    Returns:
        The decoded payload (dict-like) when validation succeeds.

    Raises:
        HTTPException: 401 for revoked/expired/invalid tokens.
    """
    try:
        # Check whether the token has been blacklisted in Redis
        if redis_client.get(f"blacklist:{token}"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def decode_refresh_token(token: str) -> dict:
    """Decode and validate a refresh token.

    Validates the token signature and expiration. Returns the payload
    dict when valid or raises `HTTPException(401)` when invalid or
    expired.

    Args:
        token: Encoded refresh token string.

    Returns:
        The decoded payload as a dict.

    Raises:
        HTTPException: 401 when the refresh token is expired or invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired",
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )
    except jwt.InvalidTokenError as e:
        # Provide a neutral error message for invalid tokens
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )