from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from src.routes import api_utils, auth



app = FastAPI(
    title="Shopito API",
    docs_url=None,
    redoc_url=None,
)

app.include_router(api_utils.router)

app.include_router(auth.router)
