from http import HTTPStatus


def test_login_for_access_token(client, user):
    response = client.post(
        "/auth/token/",
        data={"username": user.email, "password": user.clean_password},
    )

    token = response.json()["access_token"]

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "access_token": token,
        "token_type": "Bearer",
    }


def test_login_for_access_token_not_user(client):
    response = client.post(
        "/auth/token/",
        data={"username": "teste@gmail.com", "password": "123456"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password."}


def test_login_for_access_token_not_verify_password(client, user):
    response = client.post(
        "/auth/token/",
        data={"username": user.email, "password": "senhaerrada"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password."}
