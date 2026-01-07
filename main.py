from contextlib import asynccontextmanager

from fastapi import FastAPI

from src import db
from src.routes import api_utils, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.seed_database()
    yield


app = FastAPI(
    title="Shopito API",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan
)

app.include_router(api_utils.router)

app.include_router(auth.router)
