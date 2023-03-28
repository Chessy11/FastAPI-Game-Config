from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_bonus_by_id():
    response = client.get("/bonus/1")
    print(response.json())
    assert response.status_code == 200
    assert response.json()["fs_bonus_id"] == 1