import traceback
from fastapi import APIRouter, HTTPException
from app.models.query_models import AskRequest,AskResponse
from app.utils.file_utils import transcript_exists
from app.services.rag_service import answer_question
from app.services.response_service import response_service
from app.services.intent_service import detect_intent
from app.routes.summary_service import generate_summary


router = APIRouter(tags=["ask_question"])

@router.post("/ask_question",response_model=AskResponse)
def ask_question(user_question : AskRequest):
    """
    Asks question about processed youtube video, with intent aware routing
    
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
        intent = detect_intent(user_question.question)
        print("Intent detected : ",intent, "for question : ", user_question.question)
        print(f"intent : ",intent.lower())
        if intent.lower() == "summary":
            print("calling handle_summary_intent")
            json_response = handle_summary_intent(user_question.video_id, user_question.question)
            print(f"json response : ",json_response)
        else:
            json_response = handle_qa_intent(user_question.video_id, user_question.question)
            

        # json_response["intent"] = intent
        return AskResponse(
            answer=json_response['answer'],
            intent=intent
        )

    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code= 500,
            detail=f"Error processing question : {str(e)}"
        )

def handle_summary_intent(video_id : str, question : str) -> dict:
    """Handle summary intent, generate video overview"""
    try:
        print(f"handle_summary_intent")
        summary = generate_summary(video_id, question)
        print("summary", summary)
        return{
            "answer" : summary,
            "sources" : []
        }
    
    except Exception as e:
        print(f"Summary generation failed... {e}")
        return{
            "answer" : f"Error, Summary generation failed... {e}",
            "sources" : [],
            "intent" : "Summary"
        }
    
def handle_qa_intent(video_id : str, question : str) -> dict:
    """Handle QA intent, use existing RAG pipeline"""
    
    #existing RAG pipeline
    result = response_service.build_context(video_id, question, top_k=3)
    # print(result)
    prompt = response_service.build_prompt(result, question)
    # print(prompt)
    llm_response = response_service.generate_llm_response(prompt)
    # print(llm_response)
    json_response = response_service.format_response(llm_response, result)
    # print(json_response)
    # json_response["intent"] = "QA"
    # print(f"json response : ",json_response)
    
    return{
            "answer" : json_response.answer,
            "sources" : []
        }