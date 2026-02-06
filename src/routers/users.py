from __future__ import annotations
from typing import TYPE_CHECKING
from typing import List
from fastapi import APIRouter, status, Depends
from fastapi import HTTPException
from ..schemas import UserResponse, UserCreate
from ..dep import get_db
from ..crud.user import (
    db_get_user_by_id,
    db_get_all_users,
    db_create_user,
    db_update_user,
    db_delete_user,
)
from ..security.oauth2 import get_current_user

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from ..models.user import User


router = APIRouter()


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db_get_user_by_id(user_id=user_id, session=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found in DB"
        )
    return UserResponse(
        id=user.id,
        name=user.name,
        role=user.role,
        trigger_app_id=user.trigger_app_id,
    )


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db_get_all_users(session=db)
    return [
        UserResponse(
            id=user.id,
            name=user.name,
            role=user.role,
            trigger_app_id=user.trigger_app_id,
        )
        for user in users
    ]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = user.model_dump()
    new_user["role"] = "user"
    new_user = db_create_user(user_data=new_user, session=db)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to create a user"
        )
    return UserResponse(
        id=new_user.id,
        name=new_user.name,
        role=new_user.role,
        trigger_app_id=new_user.trigger_app_id,
    )


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    updated_user = db_update_user(
        user_id=user_id, user_data=user_data.model_dump(), session=db
    )
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to update user."
        )
    return UserResponse(
        id=updated_user.id,
        name=updated_user.name,
        role=updated_user.role,
        trigger_app_id=updated_user.trigger_app_id,
    )


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    is_deleted = db_delete_user(user_id=user_id, session=db)
    if is_deleted is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to delete user."
        )
    return {"Message": f"User {user_id} has been successfully deleted."}


@router.put(
    "/{user_id}/promote-to-admin",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
def promote_to_admin(
    user_id: int,
    cur_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not cur_user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized for admin promotion",
        )

    updated_user = db_update_user(
        user_id=user_id, user_data={"role": "admin"}, session=db
    )
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to update user."
        )
    return UserResponse(
        id=updated_user.id,
        name=updated_user.name,
        role=updated_user.role,
        trigger_app_id=updated_user.trigger_app_id,
    )
