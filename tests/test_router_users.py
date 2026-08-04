from http import HTTPStatus

from gerenciamento_de_biblioteca.models import User


def test_create_users(client, mock_db_time, user):
    with mock_db_time(model=User) as time:
        response = client.post(
            "/users/",
            json={
                "username": "Jose Teste",
                "email": "jose@gmail.com",
                "password": "321456",
            },
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "id": 2,
            "username": "Jose Teste",
            "email": "jose@gmail.com",
            "created_at": time.isoformat(),
            "updated_at": time.isoformat(),
        }

    response = client.post(
        "/users/",
        json={
            "username": user.username,
            "email": "fa@user.com",
            "password": "321456",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already exists."}

    response = client.post(
        "/users/",
        json={
            "username": "asd",
            "email": user.email,
            "password": "321456",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email already exists."}


def test_read_users(client, token):
    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK


def test_detail_user(client, token, user):
    response = client.get(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK


def test_detail_user_user_id_different_current_user_id(token, client):
    response = client.get(
        "/users/999", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions."}


def test_update_user(client, user, token):
    response = client.patch(
        f"/users/{user.id}/",
        json={"username": "Jose", "password": "431212ff"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["username"] == "Jose"


def test_update_user_user_id_different_current_user_id(client, token):
    response = client.patch(
        "/users/999/",
        json={"username": "Jose", "password": "431212ff"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions."}


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted successfully."}


def test_delete_user_id_different_current_user_id(client, token):
    response = client.delete(
        "/users/999/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions."}
