from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_session_chat_generate_flow() -> None:
    session = client.post("/api/session").json()["session_id"]

    first = client.post(f"/api/chat/{session}", json={"message": "Build a web app called Orbit Desk"})
    assert first.status_code == 200
    assert first.json()["ready_to_generate"] is False

    second = client.post(
        f"/api/chat/{session}",
        json={"message": "It is for support teams, with authentication dashboard and search. Deploy with docker."},
    )
    assert second.status_code == 200

    generated = client.post(f"/api/generate/{session}")
    assert generated.status_code == 200
    payload = generated.json()
    assert payload["verification"]["passed"] is True
    assert "app.py" in payload["files"]
