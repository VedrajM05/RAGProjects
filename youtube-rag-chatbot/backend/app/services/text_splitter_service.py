"""
Text Splitter Service using LangChain's RecursiveCharacterTextSplitter
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag_pipeline_config import CHUNK_SIZE,CHUNK_OVERLAP, CHUNK_SEPERATOR



def split_transcript(final_transcript : str, video_id : str) -> list[dict]:
    """
    Split transcript using LangChain's RecursiveCharacterTextSplitter()
    
    Args:
        transcript_text: The full transcript as a string
        video_id: YouTube video ID for metadata
        
    Returns:
        List of chunks with text and metadata
    """
    if not final_transcript:
        return []
    
    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP
    )

    #Actual text splitting happens here
    chunks = text_splitter.split_text(final_transcript)

    result = []
    # Now add metadata to each chunk
    for i, chunk_text in enumerate(chunks):
        chunk_data = {
            "id" : f"{video_id}_chunk_{i}",
            "text" : chunk_text,
            "meta" : {
                "video_id" : video_id,
                "chunk_index" : i, 
            }
        }
        result.append(chunk_data)
    
    return result

