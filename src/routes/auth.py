from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from src.db import DB_USERS
from src.models import Token
from src.token import create_access_token

router = APIRouter()

@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    found_user = [user for user in DB_USERS if user.username.lower() == form_data.username.lower()][0]

    if not found_user or form_data.password != found_user.password:
        raise HTTPException(status_code=401, detail="Incorrect credentials")

    access_token = create_access_token(
        username=found_user.username,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return Token(access_token=access_token, token_type="bearer")