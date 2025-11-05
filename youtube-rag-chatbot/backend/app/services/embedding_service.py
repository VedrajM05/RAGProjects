"""
Embedding Service for creating embeddings and building FAISS index
"""
import faiss
from app.rag_pipeline_config import EMBEDDING_MODEL
import numpy as np
from sentence_transformers import SentenceTransformer


# SentenceTransformer - A class from the sentence-transformers library
#                       Specialized for converting sentences/text into vector embeddings
#                       Handles popular transformer models like BERT, RoBERTa, etc.
#                       Automatically manages tokenization, model loading, and inference


#  np.ndarray : N-dimensional array from the NumPy library.
#               Fast mathematical operations - crucial for similarity search
#               Efficient memory usage - stores numbers compactly
#               FAISS compatibility - FAISS expects NumPy arrays

def create_embeddings(chunks : list[dict]) -> np.ndarray : 
    """
    Convert text chunks into dense vectors using the embedding model
    
    Args:
        chunks: List of chunk dictionaries with 'text' field
        Example: [{"id": "chunk1", "text": "chunk text here", "meta": {...}}, ...]
        
    Returns:
        numpy array of embeddings with shape (num_chunks, embedding_dimension)
    """

    if not chunks : 
        return ValueError("No chunks provided for embedding")
    
    print("Loading Embedding Model : ",str(EMBEDDING_MODEL))
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Extract text from chunks
    texts = [chunk['text'] for chunk in chunks]

    print(f"Creating embeddings for {len(texts)} chunks")

    # Create embeddings
    embeddings = model.encode(texts, show_progress_bar=True)

    print(f"Created embeddings with shape : {embeddings.shape}")
    
    return embeddings


def build_faiss_index(embeddings : np.ndarray, chunks : list[dict], video_id : str):
    """
    Builds FAISS index from string
    """

    #Create FAISS index
    dimension = embeddings.shape[1] # gives the dimension of each embedding


    #creates FAISS index that uses Inner Product (IP) as the similarity metric
    #Inner Product” = dot product between two vectors
    #The index will store all your embeddings and let you search for the most similar ones.
    index = faiss.IndexFlatIP(dimension)

    # This step normalizes each embedding vector to have L2 norm = 1.
    # So each vector becomes a unit vector.
    # cosine similarity(A,B)=A⋅B. This means cosine similarity and inner product become the same
    faiss.normalize_L2(embeddings)

    index.add(embeddings)

    return index


def search_similar(index, query_text: str, top_k: int = 3):
    """
    Search for similar chunks using query text
    """
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    # Convert query to embedding
    query_embedding = model.encode([query_text])
    
    # Normalize for cosine similarity
    faiss.normalize_L2(query_embedding)
    
    # Search
    distances, indices = index.search(query_embedding, top_k)
    
    return distances[0], indices[0]




def search_similar_embedding(index, query_embedding : np.ndarray, top_k : int = 3):
    """
    Search using existing query embedding
    """
    distances, indices = index.search(query_embedding, top_k)
    return distances[0], indices[0]


