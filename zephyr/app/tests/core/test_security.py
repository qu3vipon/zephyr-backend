from zephyr.app.core.security import create_access_token, verify_access_token


def test_access_token():
    user_id = 1

    # test create
    access_token = create_access_token(user_id)
    assert len(access_token)

    # test verify
    decoded_id = verify_access_token(access_token)
    assert decoded_id == str(user_id)
