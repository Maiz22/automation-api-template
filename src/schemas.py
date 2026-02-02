from pydantic import BaseModel, Field


class User(BaseModel):
    name: str


class UserCreate(User):
    pass


class UserResponse(User):
    id: int
    role: str


class AdminCreate(User):
    password: str = Field(min_length=8)
