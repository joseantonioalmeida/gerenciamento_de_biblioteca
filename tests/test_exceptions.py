from http import HTTPStatus

from fastapi import FastAPI
from fastapi.testclient import TestClient

from gerenciamento_de_biblioteca.exceptions import (
    global_exception_handler,
)


def test_validation_exception_handler_should_return_422(client):
    # Envia um payload inválido para a rota /users/
    response = client.post("/users/", json={})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {
        "status_code": HTTPStatus.UNPROCESSABLE_ENTITY,
        "detail": "Validation Error",
    }


def test_global_exception_handler_should_return_500():
    # Cria uma aplicação FastAPI isolada para o teste de erro 500
    test_app = FastAPI()

    # Registra o handler global que queremos testar
    test_app.add_exception_handler(Exception, global_exception_handler)

    @test_app.get("/test-error-500/")
    async def force_unexpected_error():
        raise RuntimeError("Erro simulado para teste de 500")

    # O segredo está aqui: raise_server_exceptions=False impede que o client
    # re-lance a exceção no pytest e deixa o handler retornar a
    # resposta HTTP 500
    with TestClient(test_app, raise_server_exceptions=False) as test_client:
        response = test_client.get("/test-error-500/")

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json() == {
        "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
        "detail": "Internal Server Error",
    }
