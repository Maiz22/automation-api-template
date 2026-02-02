from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routers import root, admin, user
from src.db import init_db

if TYPE_CHECKING:
    from typing import AsyncGenerator, Any


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    # Startup Logic
    init_db()

    app.include_router(prefix="", tags=["Status"], router=root.router)
    app.include_router(prefix="/admin", tags=["Admin"], router=admin.router)
    app.include_router(prefix="/user", tags=["User"], router=user.router)

    yield
    # Shutdown Logic


app = FastAPI(lifespan=lifespan)
