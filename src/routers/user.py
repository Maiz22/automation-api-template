from typing import List
from fastapi import APIRouter, status
from ..schemas import UserResponse, UserCreate


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_id():
    pass


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def get_users():
    pass


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserCreate):
    pass
