from typing import Generator, Optional

import pytz
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.requests import Request

from zephyr.app import crud, models, schemas
from zephyr.app.core import security
from zephyr.app.core.config import settings
from zephyr.app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        pay_load = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**pay_load)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_timezone(request: Request) -> pytz.timezone:
    timezone_name: Optional[str] = request.headers.get("X-Timezone")

    if timezone_name is None:
        raise HTTPException(status_code=400, detail="X-Timezone header is required.")

    if timezone_name not in pytz.all_timezones:
        raise ValidationError("Invalid timezone.")
    try:
        timezone = pytz.timezone(timezone_name)
    except pytz.exceptions.UnknownTimeZoneError:
        raise ValidationError("Invalid timezone.")

    return timezone
