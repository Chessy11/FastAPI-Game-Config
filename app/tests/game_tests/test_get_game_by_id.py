from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_game_by_id():
    response = client.get("/game/1")
    print("RESPONSEEEEEEEEEEEEEEEEEEEE",response.json())
    assert response.status_code == 200
    assert response.json()["game_id"] == 1