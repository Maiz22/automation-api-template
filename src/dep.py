from typing import Generator
from sqlalchemy.orm import Session
from .db import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Creates a Session instance passed around as dependency
    to interact with the DB. This handles the rollback and
    cleanup logic. No "with Session(engine) as session:"
    necessary in crud.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
