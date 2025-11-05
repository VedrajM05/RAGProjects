"""
Retriever Service for querying FAISS index
"""

import json
import faiss
from sentence_transformers import SentenceTransformer

from app.rag_pipeline_config import EMBEDDING_MODEL, get_faiss_directory
from app.services.embedding_service import create_embeddings


class RetrieverService:
    def __init__(self, video_id : str):
        self.video_id = video_id
        self.index = None
        self.metadata = None
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.video_id = video_id
        self.load_index(video_id)

    
    def load_index(self, video_id: str) -> bool:
        """Load FAISS index and metadata for video"""
        index_dir = get_faiss_directory(video_id)
        index_path = index_dir / "faiss_index"
        metadata_path = index_dir / "metadata.json"

        if not index_path.exists():
            return False
        
        try:
            self.index = faiss.read_index(str(index_path))
            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)

            print(f"load_index successful for video id : {video_id}")
            return True
        
        except Exception as e:
            print(f"Error loading index for video id : {video_id} : {e}")
            return False


    def retrieve(self, query : str, top_k : int =3)-> list[dict]:
        """Retrieves top_k relevant chunks for query"""

        if not self.index :
            return []
        
        # Embed user query
        query_embeddings = create_embeddings([{"text" : query}])

        faiss.normalize_L2(query_embeddings)
        
        distances, indices = self.index.search(query_embeddings, top_k)
        #Returns :         # distances = [[0.85, 0.78, 0.72]]  # Similarity scores (2D array)
                           # indices   = [[2, 0, 5]]           # Chunk indices (2D array)

        # results from FAISS search must be converted to human readable format, since vectors are difficult to understand
        # Return chunks with similarity score
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            # Why [0] indexing : Because search returns 2D arrays (even for single query)
            if idx < len(self.metadata):
                chunk_data = self.metadata[idx].copy()
                chunk_data['score'] = float(distance)
                results.append(chunk_data)
        
        return results
    

    
    
def get_retriever(video_id: str) -> RetrieverService:
    """Factory method to get retriever for video"""
    return RetrieverService(video_id)


    # def get_retriever(video_id: str) -> RetrieverService:
    # 
    # return RetrieverService(video_id)


#     {
#         "chunk_id": "video123_chunk_2",
#         "text": "This is about transformers...", 
#         "score": 0.85
#     },
#     {
#         "chunk_id": "video123_chunk_0", 
#         "text": "Machine learning basics...",
#         "score": 0.78
#     },
