from fastapi import APIRouter
import datetime
from app.core.config import config
from app.models.youtube_models import ProcessVideoRequest, ProcessVideoResponse, VideoStatus
# from app.models.query_models import AskRequest,AskResponse, SourceModel
from app.services.fetch_transcript import fetch_video_id_from_url, fetch_transcript_from_video, extract_video_id_from_playlist, get_text_from_raw_transcript
from app.utils.file_utils import save_transcript

router = APIRouter(tags=["process_video"])

@router.post("/process_video", response_model=ProcessVideoResponse)
def process_video(request : ProcessVideoRequest):
    try:
        video_id = fetch_video_id_from_url(str(request.url))
        if video_id:
            raw_transcript = fetch_transcript_from_video(video_id)
        if raw_transcript:
            final_transcript = get_text_from_raw_transcript(raw_transcript)

        if not final_transcript:
            return ProcessVideoResponse(
                video_id= video_id,
                status= VideoStatus.FAILED,
                message="Could not extract transcript from video"
            )
        
        # Save transcript
        transcript_path = save_transcript(video_id, final_transcript)

        return ProcessVideoResponse(
                video_id= video_id,
                status= VideoStatus.COMPLETED,
                message="Transcript extracted successfully"
            )
    except Exception as e:
        return ProcessVideoResponse(
                video_id=  "unknown",
                status= VideoStatus.FAILED,
                message="Transcript extraction failed"
            )


# WITHOUT ROUTERS (all in main.py) 
    # @app.get("/health")
    # @app.get("/transcript/{id}")
    # @app.post("/chat")
# Messy when you have 20+ routes

# WITH ROUTERS (organized)
    # app.include_router(health_router)      # /api/health
    # app.include_router(transcript_router)  # /api/transcript/*
    # app.include_router(chat_router)        # /api/chat/*
# Clean, modular, scalable