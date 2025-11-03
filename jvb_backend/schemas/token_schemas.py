"""Pydantic schemas for authentication tokens.

Defines the request and response shapes used by the authentication
endpoints. These schemas are intentionally small and focused on the
fields our routers and services exchange when issuing or refreshing
JWT-style tokens.
"""

from typing import Optional
from pydantic import BaseModel


class UserStatus(BaseModel):
    """Optional nested schema describing a user's online status.

    Fields:
        is_online: Whether the user is currently online.
        last_login: ISO-8601 timestamp (string) of the user's last login.
    """

    is_online: bool
    last_login: str


class TokenData(BaseModel):
    """Schema returned after successful authentication.

    Fields:
        message: Friendly message or status.
        access_token: Short-lived access token (JWT or similar).
        refresh_token: Long-lived refresh token used to obtain new access
                       tokens.
        token_type: Token type string (defaults to "bearer").
        user_status: Optional `UserStatus` providing presence info.
    """

    message: str
    access_token: str
    refresh_token: str
    # Default is the string "bearer" (not a tuple). The trailing comma
    # in the original file accidentally created a single-item tuple.
    token_type: str = "bearer"
    user_status: Optional[UserStatus] = None


class RefreshTokenRequest(BaseModel):
    """Request payload for refreshing an access token.

    Fields:
        refresh_token: The refresh token previously issued to the client.
    """

    refresh_token: str


class RefreshTokenData(BaseModel):
    """Response payload returned when issuing a new access token via a
    refresh operation.

    Fields:
        access_token: Newly issued access token.
        token_type: Token type string, typically "bearer".
    """

    access_token: str
    token_type: str = "bearer"