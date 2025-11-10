import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ingest_valid_record():
    data = {"id": 99, "name": "Sensor Test", "value": 12.5}
    response = client.post("/ingest", json=data)
    assert response.status_code == 200
    assert "Record stored successfully" in response.json()["message"]

def test_ingest_duplicate_record():
    data = {"id": 1, "name": "Sensor Test", "value": 12.5}
    response = client.post("/ingest", json=data)
    assert response.status_code == 400
