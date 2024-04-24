from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_symbol_config():
    data = {
        "game_id": 1,
        "symbol_name": "Test Symbol",
        "symbol_type": 1
    }
    response = client.post("/create-symbol", json=data)
    assert response.status_code == 201
    assert response.json()["symbol_name"] == "Test Symbol"
