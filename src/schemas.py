from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class User(BaseModel):
    name: str


class UserCreate(User):
    trigger_app_id: Optional[str] = None


class UserResponse(User):
    id: int
    role: str
    trigger_app_id: Optional[str]


class AdminCreate(User):
    password: str = Field(min_length=8)
    bootstrap_token: str


class TokenData(BaseModel):
    id: int
