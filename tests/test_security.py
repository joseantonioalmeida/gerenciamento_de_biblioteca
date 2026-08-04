import pytest
from jwt import decode

from gerenciamento_de_biblioteca.security import (
    create_access_token,
)


@pytest.mark.asyncio
async def test_jwt(settings):
    token = create_access_token(data={"mensagem": "test"})

    decoded = decode(token, settings.SECRET_KEY, settings.ALGORITHM)

    assert decoded["mensagem"] == "test"
    assert "exp" in decoded
