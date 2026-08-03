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
