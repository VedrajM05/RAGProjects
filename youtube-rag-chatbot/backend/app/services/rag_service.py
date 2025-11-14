from app.models.query_models import AskResponse


def answer_question_stub(video_id : str, question : str) -> AskResponse :
    """
    This method invokes actual rag pipeline
    Currently returning canned response, will be replaced with actual RAG pipeline later
    Args:
        video_id: YouTube video ID
        question: User's question about the video
        
    Returns:
        AskResponse with answer and sources
    """
    # Canned response create
    # sources = [
    #     SourceModel(
    #         start=120.5,
    #         duration=45.2,
    #         text=f"Based on video content, this question discusses topics related to '{question}'.",
    #         score=0.95
    #     ),
    #     SourceModel(
    #         start=121.5,
    #         duration=41.2,
    #         text=f"Based on video content, this is another relevant topic related to '{question}'.",
    #         score=0.87
    #     )
    # ]

    return AskResponse(
        answer=f"This is a stub response for video id : '{video_id}'. The RAG pipeline will be implemented later",
        #sources=sources
    )



def answer_question(video_id : str, question : str) -> AskResponse :
    """
    Real RAG logic will be implemented later here
    
    Args:
        video_id: YouTube video ID
        question: User's question about the video
        
    Returns:
        AskResponse with answer and sources

    """
    return answer_question_stub(video_id, question)