from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from zephyr.app import crud, schemas
from zephyr.app.api import deps
from zephyr.app.core import security
from zephyr.app.core.security import get_password_hash, verify_access_token

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return {
        "access_token": security.create_access_token(user.id),
        "token_type": "bearer",
    }


@router.post("/sign-up", response_model=schemas.UserOut, status_code=201)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    # if settings.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )

    user_out = user.as_dict()
    user_out.update({"access_token": security.create_access_token(user.id)})
    return user_out


@router.post("/reset-password", response_model=schemas.Msg)
def reset_password(
    access_token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    user_id = verify_access_token(access_token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail="The user with this username does not exist."
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.password_hash = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully."}
