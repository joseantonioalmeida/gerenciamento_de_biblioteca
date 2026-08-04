from http import HTTPStatus

import pytest
from freezegun import freeze_time
from jwt import decode, encode

from gerenciamento_de_biblioteca.security import (
    create_access_token,
)


@pytest.mark.asyncio
async def test_jwt(settings):
    token = create_access_token(data={"mensagem": "test"})

    decoded = decode(token, settings.SECRET_KEY, settings.ALGORITHM)

    assert decoded["mensagem"] == "test"
    assert "exp" in decoded


def test_invalid_jwt_exception_decode_error(client):
    response = client.get(
        "/users/", headers={"Authorization": "Bearer token-invalid"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials."}


def test_token_invalid_not_subject_email(client):
    token_sem_sub = create_access_token(data={})
    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {token_sem_sub}"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials."}


def test_token_expired_after_time(client, user):
    with freeze_time("2026-08-04 12:00:00"):
        response = client.post(
            "/auth/token/",
            data={"username": user.email, "password": user.clean_password},
        )

        token_expired = response.json()["access_token"]

        assert response.status_code == HTTPStatus.OK

    with freeze_time("2026-08-04 12:30:00"):
        response = client.patch(
            f"/users/{user.id}/",
            data={"username": user.email, "password": user.clean_password},
            headers={"Authorization": f"Bearer {token_expired}"},
        )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials."}


def test_get_current_user_not_found(client, settings):
    data = {"sub": "nao_existo@example.com"}
    token = encode(data, settings.SECRET_KEY, settings.ALGORITHM)

    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials."}
