from fastapi.testclient import TestClient
from main import app

import pytest


@pytest.fixture(scope="function")
def ac():
    "Асинхронный клиент для тестирования эндпоинтов"
    with TestClient(app=app, base_url="http://test") as ac:
        yield ac