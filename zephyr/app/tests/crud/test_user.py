from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from zephyr.app import crud
from zephyr.app.schemas import UserCreate
from zephyr.app.tests.utils.user import random_string_16


class TestUserCRUD:
    def test_create_user(self, db: Session):
        username = random_string_16()
        password = random_string_16()
        user_in = UserCreate(username=username, password=password)
        user = crud.user.create(db, obj_in=user_in)
        assert user.username == username
        assert hasattr(user, "password_hash")

    def test_get_user(self, db: Session, test_user):
        user_get = crud.user.get(db, id=test_user.id)
        assert user_get
        assert user_get.uuid == test_user.uuid
        assert jsonable_encoder(user_get) == jsonable_encoder(test_user)

    def test_get_user_by_username(self, db: Session, test_user):
        user_get = crud.user.get_by_username(db, username=test_user.username)
        assert user_get
        assert user_get.uuid == test_user.uuid
        assert jsonable_encoder(user_get) == jsonable_encoder(test_user)

    def test_authenticate_user(self, db: Session, test_user, test_user_raw_password):
        authenticated_user = crud.user.authenticate(
            db, username=test_user.username, password=test_user_raw_password
        )
        assert authenticated_user
        assert authenticated_user.uuid == test_user.uuid
        assert jsonable_encoder(authenticated_user) == jsonable_encoder(test_user)
