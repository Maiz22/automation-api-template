from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select, update, insert, delete
from ..models import User
import logging

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from typing import Sequence

logger = logging.getLogger("uvicorn")


def db_get_user_by_id(user_id: int, session: Session) -> User | None:
    statement = select(User).where(User.id == user_id)
    return session.execute(statement).scalar_one_or_none()


def db_get_user_by_username(username: str, session: Session) -> User | None:
    statement = select(User).where(User.username == username)
    return session.execute(statement).scalar_one_or_none()


def db_get_all_users(session: Session) -> Sequence[User]:
    statement = select(User)
    return session.execute(statement).scalars().all()


def db_create_user(user_data: dict, session: Session) -> User | None:
    try:
        statement = insert(User).values(**user_data).returning(User)
        new_user = session.scalar(statement)
        session.commit()
        session.refresh(new_user)
    except IntegrityError as e:
        logger.error(e)
        return None
    return new_user


def db_update_user(user_id: int, user_data: dict, session: Session) -> User | None:
    statement = (
        update(User).where(User.id == user_id).values(**user_data).returning(User)
    )
    updated_user = session.execute(statement).scalar_one_or_none()
    if not updated_user:
        return None

    session.commit()
    return updated_user


def db_delete_user(user_id: int, session: Session) -> bool:
    stmt = delete(User).where(User.id == user_id)
    result = session.execute(stmt)

    deleted = (result.rowcount or 0) > 0  # type: ignore
    if deleted:
        session.commit()
    return deleted


def db_check_admin_exists(session: Session) -> bool:
    statement = select(User).where(User.role == "admin")
    result = session.execute(statement).scalars().first()
    return True if result else False
