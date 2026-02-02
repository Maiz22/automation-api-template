from fastapi import APIRouter, status
from ..schemas import AdminCreate


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AdminCreate)
async def create_admin():
    pass


@router.post("/login", status_code=status.HTTP_200_OK)
async def admin_login():
    pass


@router.post("/logout", status_code=status.HTTP_200_OK)
async def admin_logout():
    pass
