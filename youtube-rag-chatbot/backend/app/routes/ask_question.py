from fastapi import APIRouter, HTTPException
from app.models.query_models import AskRequest,AskResponse
from app.utils.file_utils import transcript_exists
from app.services.rag_service import answer_question
from app.services.response_service import response_service


router = APIRouter(tags=["ask_question"])

@router.post("/ask_question",response_model=AskResponse)
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
        # response = answer_question(user_question.video_id, user_question.question)
        # return response
        result = response_service.build_context(user_question.video_id, user_question.question, top_k=3)
        print(result)
        prompt = response_service.build_prompt(result, user_question.question)
        print(prompt)
        llm_response = response_service.generate_llm_response(prompt)
        print(llm_response)
        json_response = response_service.format_response(llm_response, result)
        print(json_response)
        return json_response
    
    except Exception as e:
        raise HTTPException(
            status_code= 500,
            detail=f"Error processing question : {str(e)}"
        )


    
