from fastapi import APIRouter
import datetime
from app.core.config import config
from app.models.youtube_models import ProcessVideoRequest, ProcessVideoResponse
from app.models.query_models import AskRequest,AskResponse

router = APIRouter(tags=["health"])

@router.get("/health")
def health_check():
    return {
        "health" : "healthy",
        "timestamp" : datetime.datetime.now().isoformat(),
        "version" : config.VERSION, 
        "title" : config.APP_NAME
    }



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