import os
import sys
from fastapi import FastAPI
from fastapi.testclient import TestClient

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
BACKEND_ROOT = os.path.join(PROJECT_ROOT, "backend")

for path in (PROJECT_ROOT, BACKEND_ROOT):
    if path not in sys.path:
        sys.path.insert(0, path)

import backend.app.routes.process_video as process_video_module
from app.models.youtube_models import ProcessVideoRequest, ProcessVideoResponse, VideoStatus

# app = FastAPI()
# app.include_router(router)
# client = TestClient(app)

def test_process_video_success_unit(monkeypatch):
    
    #Arrange : fake out all dependencies and internal methods which are called inside process_video API
    def fake_fetch_video_id_from_url(url : str) -> str:
        return "fake_video_id"
    
    def fake_fetch_transcript_from_video(video_id : str):
        return ["raw", "transcript", "chunks"]
    
    def fake_get_text_from_raw_transcript(raw_transcript) -> str:
        return "final transcript text"
    
    
    def fake_save_transcript(video_id : str, text : str) -> str:
        return "fake/path/transcript.txt"
    
    monkeypatch.setattr(process_video_module, "fetch_video_id_from_url", fake_fetch_video_id_from_url)
    monkeypatch.setattr(process_video_module, "fetch_transcript_from_video", fake_fetch_transcript_from_video)
    monkeypatch.setattr(process_video_module, "get_text_from_raw_transcript", fake_get_text_from_raw_transcript)
    monkeypatch.setattr(process_video_module, "save_transcript", fake_save_transcript)
    
    #Act : call API
    # payload = {"url" : "https://www.youtube.com/watch?v=anything"}
    # response = client.post("/process_video", json = payload)
    request = ProcessVideoRequest(url="https://www.youtube.com/watch?v=anything")
    response : ProcessVideoRequest = process_video_module.process_video(request)
    
    #Assert : check the response
    assert isinstance(response, ProcessVideoResponse)
    #assert response.status_code == 200
    # data = response.json()

    assert response.video_id == "fake_video_id"
    assert response.status == "COMPLETED"
    assert response.message == "Transcript extracted successfully"



def test_process_video_exception_unit(monkeypatch):
    
    #Arrange : fake out all dependencies and internal methods which are called inside process_video API
    def fake_fetch_video_id_from_url(url : str) -> str:
        return "fake_video_id"
    
    def fake_fetch_transcript_from_video(video_id : str):
        return ["raw", "transcript", "chunks"]
    
    def fake_get_text_from_raw_transcript(raw_transcript) -> str:
        raise RuntimeError("Disk is full")
    
    
    def fake_save_transcript(video_id : str, text : str) -> str:
        return "fake/path/transcript.txt"
    
    monkeypatch.setattr(process_video_module, "fetch_video_id_from_url", fake_fetch_video_id_from_url)
    monkeypatch.setattr(process_video_module, "fetch_transcript_from_video", fake_fetch_transcript_from_video)
    monkeypatch.setattr(process_video_module, "get_text_from_raw_transcript", fake_get_text_from_raw_transcript)
    monkeypatch.setattr(process_video_module, "save_transcript", fake_save_transcript)
    
    #Act : call API
    # payload = {"url" : "https://www.youtube.com/watch?v=anything"}
    # response = client.post("/process_video", json = payload)
    request = ProcessVideoRequest(url="https://www.youtube.com/watch?v=anything")
    response : ProcessVideoRequest = process_video_module.process_video(request)
    
    #Assert : check the response
    assert isinstance(response, ProcessVideoResponse)

    assert response.video_id == "fake_video_id"
    assert response.status == VideoStatus.FAILED
    assert response.message == "Transcript extraction failed"