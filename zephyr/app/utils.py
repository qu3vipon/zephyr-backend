from typing import Optional

from jose import jwt

from zephyr.app.core import security
from zephyr.app.core.config import settings


def verify_access_token(access_token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        return decoded_token["sub"]
    except jwt.JWTError:
        return None
