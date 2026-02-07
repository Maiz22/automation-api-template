from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from typing import Annotated
from ..schemas import TokenData
from ..config import settings
from ..crud.user import db_get_user_by_id
from ..dep import get_db

# from ..crud.user import db_get_user_by_id
from ..models import User

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

# OAuth2 instance (scheme) that can be used as dependency to validate the Bearer token.
# The tokenURL is the path that is used to create the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Takes a token relevant data and an optional expiration date
    sets the expiration data or falls back to default 15 minutes.
    Adds the expiration date to the data, takes the SECRET_KEY and
    JWT_ALGORITHM to create the token.
    Returns the jwt.
    """
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        data_to_encode, settings.jwt_secret_key, settings.jwt_algorithm
    )
    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> TokenData:
    """
    Verifies the access token. Takes the token data, SECRET_KEY and algorithm
    used to create the certificate. Decodes the token, creates a test signature
    compares test signature with token signature. jwt.decode raises exceptions
    if certificate does not match or if it is expired.
    Returns token_data in case the token is valid.
    """
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=settings.jwt_algorithm
        )
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    return token_data


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> User | None:
    """
    Takes a bearer token that is required to follow the oauth2_scheme.
    Returns a user instance, if verification and user extraction are successful.
    Raises credential exception if no user could be found in db.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = db_get_user_by_id(user_id=token_data.id, session=db)
    if user is None:
        raise credentials_exception
    return user
