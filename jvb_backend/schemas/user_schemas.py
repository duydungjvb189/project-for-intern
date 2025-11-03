"""Pydantic schemas for user-related requests and responses.

This module defines the request/response shapes used by user routes and
authentication services. Schemas keep external API contracts stable and
validate inputs coming from clients.
"""

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Schema for creating a new user account.

    Fields:
        username: Desired unique username for the account.
        email: Validated email address (uses Pydantic's EmailStr).
        password: Plaintext password provided by the client; callers
                  must hash this before persisting.
    """

    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Schema for a login request.

    Clients provide username and password for authentication. Passwords
    should be compared to stored hashes using a secure verifier in the
    authentication service.
    """

    username: str
    password: str


class UserResponse(BaseModel):
    """Schema returned to clients when sending user data.

    Includes identifying fields but intentionally excludes sensitive data
    such as `password` or `password_hash`.
    """

    id: int
    username: str
    email: EmailStr

    class Config:
        # Enable population from ORM objects (SQLAlchemy) when converting
        # DB models to response schemas. In Pydantic v2 this is `from_attributes`.
        from_attributes = True