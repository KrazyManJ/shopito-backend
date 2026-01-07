from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from starlette import status

from src import db
from src.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from src.db import User
from src.models import Token, UserInfo
from src.token import decode_access_token, create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


async def verify_authentication(username: str, input_password: str) -> bool:
    first_found_user = await db.get_user_by_username(username)
    return first_found_user and verify_password(input_password, first_found_user.password_hash)


async def get_current_user_info(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInfo:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    first_found_user = await db.get_user_by_username(payload.username)
    if first_found_user is None:
        raise HTTPException(status_code=404, detail="Not found")

    return UserInfo(**first_found_user.model_dump())
