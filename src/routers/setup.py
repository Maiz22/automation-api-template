from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import APIRouter, status, Depends, HTTPException
from ..schemas import AdminCreate, UserResponse
from ..dep import get_db
from ..crud.user import db_create_user, db_check_admin_exists
from ..config import settings

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/admin", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def admin_setup(user: AdminCreate, db: Session = Depends(get_db)):
    if db_check_admin_exists:
        raise HTTPException(status_code=403, detail="Unable to create admin")
    if user.bootstrap_token != settings.bootstrap_token:
        raise HTTPException(status_code=403, detail="Unable to create admin")
    new_user = user.model_dump()
    new_user["role"] = "admin"
    new_user = db_create_user(user_data=new_user, session=db)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to create a admin"
        )
    return UserResponse(
        id=new_user.id,
        name=new_user.name,
        role=new_user.role,
        trigger_app_id=new_user.trigger_app_id,
    )


@router.post("/login", status_code=status.HTTP_200_OK)
async def admin_login(db: Session = Depends(get_db)):
    pass


@router.post("/logout", status_code=status.HTTP_200_OK)
async def admin_logout():
    pass
