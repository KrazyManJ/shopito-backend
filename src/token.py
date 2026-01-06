from datetime import datetime, timezone, timedelta

import jwt

from src.constants import SECRET_KEY, ALGORITHM


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