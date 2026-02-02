from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import settings
import logging


if TYPE_CHECKING:
    from sqlalchemy import Engine

# Use uvicorns logging
logger = logging.getLogger("uvicorn")


# Create Base class inheriting from DeclarativeBase. Import inside models to register them here.
class Base(DeclarativeBase):
    pass


def create_postgres_engine() -> Engine:
    if settings.mode == "dev":
        logger.info("Create DB engine in development mode.")
        echo = True
        url = f"postgresql://{settings.db_user}:{settings.db_pw}@{settings.db_host}/{settings.db_name}"
    elif settings.mode == "prod":
        logger.info("Create DB engine in production mode.")
        echo = False
        url = f"postgresql://{settings.db_user}:{settings.db_pw}@{settings.db_service_name}:{settings.db_port}/{settings.db_name}"
    else:
        logger.error("Invalid mode set. Please check your ENV.")
        raise ValueError("Invalid mode set in ENV")
    return create_engine(url=url, echo=echo)


# Create the postgres engine
engine = create_postgres_engine()
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def init_db() -> None:
    import src.models

    Base.metadata.create_all(bind=engine)
