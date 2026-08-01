def test_read_root_should_return_a_dictionary(client) -> None:
    response = client.get("/")

    assert response.json() == {
        "message": "Bem vindo a API de gerenciamento de biblioteca!"
    }
