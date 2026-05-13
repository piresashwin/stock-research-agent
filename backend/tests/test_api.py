from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_trigger_research_job():
    res = client.post("/api/research", json={"symbol": "MARUTI"})
    assert res.status_code == 200
    data = res.json()
    assert data["symbol"] == "MARUTI"
    assert data["status"] in ["pending", "gathering", "completed", "failed"]

def test_list_researched_stocks():
    res = client.get("/api/research")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_get_research_state_not_found():
    res = client.get("/api/research/UNKNOWN_SYMBOL_TEST_404")
    assert res.status_code == 404

def test_stream_endpoint_status():
    # Trigger job first to guarantee DB state row initialization
    client.post("/api/research", json={"symbol": "TCS"})
    
    # Consuming stream connection directly returns 200 chunk headers
    with client.stream("GET", "/api/research/TCS/stream") as response:
        assert response.status_code == 200
        # Read initial chunk delta bytes
        chunk = next(response.iter_text())
        assert "data:" in chunk or "type" in chunk
