from typing import List, Optional
from pydantic import BaseModel, Field



class SourceModel(BaseModel):
    """Response model individual source segment about the youtube video"""
    start : float = Field(...,description="Start time in seconds", ge=0)
    duration : float = Field(...,  description="Duration in seconds", ge=0)
    text : str = Field(...,  description="Transcript text from this segment")
    score : Optional[float] = Field(None,  description="Relevance score (0-1), higher is more relevant", ge=0, le=1)

class AskRequest(BaseModel):
    """Request model for asking questions about the youtube video"""
    video_id : str = Field(..., min_length=1, description="Youtube video id", examples="video123")
    question : str = Field(..., min_length=1, description="Question to ask about the video", examples="What is this video about?")

class AskResponse(BaseModel):
    """Response model for question answers with sources"""
    answer : str = Field(...,  description="Generated answer to the question")
    sources : List[SourceModel] = Field(..., description="Source segments supporting the answer")