from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src import validation
from src.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from src.models import Token, User, UserInfo
from src.token import create_access_token

router = APIRouter(tags=["Auth"])

@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    if not validation.verify_authentication(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return Token(
        access_token=create_access_token(
            username=form_data.username,
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        ),
        token_type="bearer"
    )

@router.get("/me")
async def get_me(
        user: Annotated[UserInfo, Depends(validation.get_current_user_info)]
) -> UserInfo:
    return user