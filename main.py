from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from src.routes import api_utils, auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(
    title="Shopito API",
    docs_url=None,
    redoc_url=None,
)

app.include_router(api_utils.router)

app.include_router(auth.router)
