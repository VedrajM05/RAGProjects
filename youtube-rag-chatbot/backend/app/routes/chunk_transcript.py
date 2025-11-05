# Implement Text Splitter
from fastapi import APIRouter, HTTPException
from app.utils.file_utils import load_transcript_text
from app.services.text_splitter_service import split_transcript
from app.services.embedding_service import create_embeddings, build_faiss_index, search_similar_embedding, search_similar


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

        # 1 : create embeddings
        embeddings = create_embeddings(chunks)
        
        # 2 : Build FAISS index
        print("Build FAISS index")
        index = build_faiss_index(embeddings, chunks, video_id)

        # 3 User query 
        query = "What is RAG?"

        #4 : create embeddings for user query
        # distances, indices = search_similar(index, query, top_k=3)
        query_embeddings = create_embeddings([{"text" : query}])


        distances, indices = search_similar_embedding(index, query_embeddings, top_k=3)

        print(f"Index has vectors ready for search", index)

        # prints data
        print("Top similar chunks:")
        for i , (dist, idx) in enumerate(zip(distances, indices)):
            chunk = chunks[idx]
            print(f"{i + 1}. Score: {dist : .3f} - {chunk['text'][:100]}...")



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


    
