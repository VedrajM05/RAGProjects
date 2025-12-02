import os
import sys
from fastapi import FastAPI
from fastapi.testclient import TestClient

# ----------------------------
# Fix import paths for tests
# ----------------------------
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
BACKEND_ROOT = os.path.join(PROJECT_ROOT, "backend")

for path in (PROJECT_ROOT, BACKEND_ROOT):
    if path not in sys.path:
        sys.path.insert(0, path)

# Now:
#   - "backend" is importable (backend/*)
#   - "app" is importable (backend/app/*)
#     so 'from app.models...' inside process_video.py works.

import backend.app.routes.process_video as process_video_module
from backend.app.routes.process_video import router

# Build a small FastAPI app and attach this router
app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_process_video_http_success(monkeypatch):
    # Arrange: fake all dependencies used inside process_video()

    def fake_fetch_video_id_from_url(url: str) -> str:
        return "fake_video_id"

    def fake_fetch_transcript_from_video(video_id: str):
        return ["raw", "transcript", "chunks"]

    def fake_get_text_from_raw_transcript(raw_transcript) -> str:
        return "final transcript text"

    def fake_save_transcript(video_id: str, text: str) -> str:
        return "fake/path/transcript.txt"

    # Patch functions on the *module* object
    monkeypatch.setattr(process_video_module, "fetch_video_id_from_url", fake_fetch_video_id_from_url)
    monkeypatch.setattr(process_video_module, "fetch_transcript_from_video", fake_fetch_transcript_from_video)
    monkeypatch.setattr(process_video_module, "get_text_from_raw_transcript", fake_get_text_from_raw_transcript)
    monkeypatch.setattr(process_video_module, "save_transcript", fake_save_transcript)

    # Act: call the API through HTTP
    payload = {"url": "https://www.youtube.com/watch?v=anything"}
    response = client.post("/process_video", json=payload)
    print(response)
    # Assert: HTTP + JSON response
    assert response.status_code == 200
    data = response.json()

    assert data["video_id"] == "fake_video_id"
    assert data["status"] == "COMPLETED"
    assert data["message"] == "Transcript extracted successfully"


def test_process_video_http_failed(monkeypatch):
    # Arrange: fake all dependencies used inside process_video()

    def fake_fetch_video_id_from_url(url: str) -> str:
        return "fake_video_id"

    def fake_fetch_transcript_from_video(video_id: str):
        return ["raw", "transcript", "chunks"]

    def fake_get_text_from_raw_transcript(raw_transcript) -> str:
        return ""

    def fake_save_transcript(video_id: str, text: str) -> str:
        return "fake/path/transcript.txt"

    # Patch functions on the *module* object
    monkeypatch.setattr(process_video_module, "fetch_video_id_from_url", fake_fetch_video_id_from_url)
    monkeypatch.setattr(process_video_module, "fetch_transcript_from_video", fake_fetch_transcript_from_video)
    monkeypatch.setattr(process_video_module, "get_text_from_raw_transcript", fake_get_text_from_raw_transcript)
    monkeypatch.setattr(process_video_module, "save_transcript", fake_save_transcript)

    # Act: call the API through HTTP
    payload = {"url": "https://www.youtube.com/watch?v=anything"}
    response = client.post("/process_video", json=payload)
    print(response)
    # Assert: HTTP + JSON response
    assert response.status_code == 200
    data = response.json()

    assert data["video_id"] == "fake_video_id"
    assert data["status"] == "FAILED"
    assert data["message"] == "Could not extract transcript from video"