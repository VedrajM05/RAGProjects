from fastapi import APIRouter, HTTPException
from app.models.query_models import AskRequest,AskResponse
from app.utils.file_utils import transcript_exists, load_transcript_text
from app.services.text_splitter_service import split_transcript


router = APIRouter(tags=["chunk_transcript"])

@router.post("/chunk_transcript/{video_id}")
def chunk_transcript(video_id : str):
    
    try:
        transcript_text = load_transcript_text(video_id)
        if not transcript_text:
            raise HTTPException(
                status_code = 404,
                detail=f"No transcript found locally. Please process the video to store transcript"
            )
        
        chunks = split_transcript(transcript_text, video_id)

        return {
            "video_id" : video_id,
            "chunk_count" : len(chunks),
            "chunks" : chunks
        }
    
    except Exception as e:
        raise HTTPException(
            status_code= 500,
            detail=f"Error processing transcript : {str(e)}"
        )


    
