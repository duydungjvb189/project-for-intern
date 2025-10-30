from typing import Optional
from pydantic import BaseModel

class UserStatus(BaseModel):
    is_online: bool
    last_login: str

class TokenData(BaseModel):
    message: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer",
    user_status: Optional[UserStatus] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RefreshTokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"