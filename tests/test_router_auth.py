from http import HTTPStatus

from freezegun import freeze_time


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


def test_refresh_token(client, token):
    response = client.post(
        "/auth/refresh-token/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "Bearer"


def test_token_expired_dont_refresh(client, user):
    with freeze_time("2026-08-04 12:00:00"):
        response = client.post(
            "/auth/token/",
            data={"username": user.email, "password": user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2026-08-04 12:30:00"):
        response = client.post(
            "/auth/refresh-token/",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials."}
