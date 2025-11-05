# Implement Text Splitter
from fastapi import APIRouter, HTTPException
from app.utils.file_utils import load_transcript_text
from app.services.text_splitter_service import split_transcript
from app.services.embedding_service import create_embeddings, build_faiss_index, search_similar_embedding, persist_index
from app.services.retriever_service import get_retriever


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

        # 3. User query 
        query = "What is RAG?"

        # 4. Persist index to disk
        index_path = persist_index(index, chunks, video_id)        
        print(f"Index persisted to path : {index_path}")

        # 5. Get retriever for video
        retriever = get_retriever(video_id)

        # Retrieve relevant chunks
        results = retriever.retrieve(query, top_k = 3)

        print(f"Top similar chunks for query : {query}")
        for result in results:
            print(f"Score : {result['score']: .3f}")
            print(f"Text : {result['text']}")
            print("-------------")

        # region Commented code
        # #5 : create embeddings for user query
        # # distances, indices = search_similar(index, query, top_k=3)
        # query_embeddings = create_embeddings([{"text" : query}])


        # distances, indices = search_similar_embedding(index, query_embeddings, top_k=3)

        # print(f"Index has vectors ready for search", index)


        # endregion Commented code




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


    
