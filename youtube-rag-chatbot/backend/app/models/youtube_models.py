# Define the data contracts the frontend will use.
from enum import Enum
from typing import Optional
from pydantic import BaseModel, HttpUrl

class VideoStatus(str, Enum):
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ProcessVideoRequest(BaseModel):
    """Request model for video processing endpoint"""
    url : HttpUrl


class ProcessVideoResponse(BaseModel):
    """Response model for video processing endpoint"""
    video_id : str
    status : VideoStatus
    message : Optional[str] = None

class Config:
    # This makes the enum values serialized as strings in JSON
    use_enum_values = True
