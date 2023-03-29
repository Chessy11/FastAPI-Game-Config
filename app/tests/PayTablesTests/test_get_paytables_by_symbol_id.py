from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_paytables_by_symbol_id():
    response = client.get("/paytables/1")
    assert response.status_code == 200
