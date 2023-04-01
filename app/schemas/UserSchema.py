from pydantic import BaseModel
from typing import Optional


class UserInSchema(BaseModel):
    username: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserOutSchema(BaseModel):
    user_id: int
    username: str
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
