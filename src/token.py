from datetime import datetime, timezone, timedelta

import jwt
from jwt import InvalidTokenError

from src.constants import SECRET_KEY, ALGORITHM
from src.models import TokenData


def create_access_token(
        username: str,
        expires_delta: timedelta
):
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + expires_delta
    }

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(
            username=payload.get("sub")
        )
    except InvalidTokenError:
        return None