from fastapi import APIRouter, HTTPException
from app.models.query_models import AskRequest,AskResponse
from app.utils.file_utils import transcript_exists
from app.services.rag_service import answer_question


router = APIRouter(tags=["ask_question"])

@router.post("/ask_question", response_model=AskResponse)
def ask_question(user_question : AskRequest):
    """
    Asks question about processed youtube video
    
    Args:
        video_id: YouTube video ID
        question: User's question about the video
        
    Returns:
        AskResponse model i.e. answer with sources from video transcript with answer and sources

    """
    # Validate that the video has been processed
    if  not transcript_exists(user_question.video_id) :
        raise HTTPException(
            status_code= 404,
            detail=f"Video Id : '{user_question.video_id}' not found. Please process the video first and then ask questions"
        )
    
    try:
        response = answer_question(user_question.video_id, user_question.question)
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code= 500,
            detail=f"Error processing question : {str(e)}"
        )


    
