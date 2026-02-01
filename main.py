from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routers import root

if TYPE_CHECKING:
    from typing import AsyncGenerator, Any


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    # Startup Logic

    app.include_router(prefix="", tags=["Status"], router=root.router)
    yield
    # Shutdown Logic


app = FastAPI(lifespan=lifespan)
