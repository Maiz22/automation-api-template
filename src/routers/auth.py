from __future__ import annotations
from typing import TYPE_CHECKING, Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..dep import get_db
from ..crud.user import db_get_user_by_username
from ..security.password import verify_password
from ..security.oauth2 import create_access_token
from ..schemas import TokenCreate

if TYPE_CHECKING:
    from ..models.user import User
    from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenCreate)
def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    # if is_locked_out(username=user_credentials.username):
    #    raise HTTPException(
    #        status_code=429, detail="Too many login attempts. Try again later."
    #    )
    user = db_get_user_by_username(username=user_credentials.username, session=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
    if not verify_password(
        plain_password=user_credentials.password, hashed_password=user.password_hash
    ):
        # register_failed_attempt(username=user_credentials.username)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"user_id": user.id})
    return TokenCreate(access_token=access_token, token_type="bearer")


def logout():
    pass
