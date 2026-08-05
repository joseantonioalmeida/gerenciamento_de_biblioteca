import logging
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.testclient import TestClient

from gerenciamento_de_biblioteca.middleaware import LoggingMiddleware


def test_logging_middleware_should_log_request_details(caplog):
    # Define o nível de captura do caplog para o logger do middleware
    caplog.set_level(logging.INFO, logger="api.requests")

    test_app = FastAPI()
    test_app.add_middleware(LoggingMiddleware)

    @test_app.get("/ping/")
    async def ping():
        return {"message": "pong"}

    client = TestClient(test_app)
    response = client.get("/ping/")

    # 1. Valida que a resposta da requisição continua intacta
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "pong"}

    # 2. Valida o conteúdo registrado pelo logger
    assert "LoggingMiddleware | GET /ping/ -> Status: 200" in caplog.text
    assert "Processed in" in caplog.text


def test_logging_middleware_should_log_errors(caplog):
    caplog.set_level(logging.INFO, logger="api.requests")

    test_app = FastAPI()
    test_app.add_middleware(LoggingMiddleware)

    @test_app.post("/not-found/")
    async def not_found():
        pass

    # Usamos raise_server_exceptions=False para testar respostas de erro
    # genéricas
    client = TestClient(test_app, raise_server_exceptions=False)
    response = client.get("/not-found/")

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert "LoggingMiddleware | GET /not-found/ -> Status: 405" in caplog.text
