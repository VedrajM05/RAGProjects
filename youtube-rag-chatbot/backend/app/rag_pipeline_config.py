"""
Central configuration for the YouTube RAG Pipeline

This module contains all constants and tunable parameters for the RAG system.
Allows for easy configuration changes without modifying code logic.
"""

from pathlib import Path

# Embedding Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384 # Number of features used to describe an item.
EMBEDDING_MAX_LENGTH = 256 # Max number of tokens an embedding model can accept in a single input

# Vector Store Configuration
VECTOR_STORE_BASE_DIR = Path("./app/vector_store")
FAISS_INDEX_NAME = "faiss_index"

# Text Chunking Configuration
CHUNK_SIZE = 100 # No of characters per chunk
CHUNK_OVERLAP = 20 # Overlap between 2 consecutive chunks
CHUNK_SEPERATOR = "\n" # Seperator for splitting text

# Retrieval Configuration
TOP_K = 3 # No of relevant chunks to retrieve per query
SEARCH_TYPE = "similarity" # Options : similarity, MMR, MQR

# LLM Configuration
LLM_MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"


def get_faiss_directory(video_id : str) -> Path :
    """
    Get the FAISS vector store directory for a specific video
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Path to the video-specific vector store directory
    """
    return VECTOR_STORE_BASE_DIR / video_id



class RAGConfig:
    """Configuration class for RAG pipeline settings"""
    def __init__(self):
        self.embedding_model = EMBEDDING_MODEL
        self.embedding_dimension = EMBEDDING_DIMENSION
        self.chunk_size = CHUNK_SIZE
        self.chunk_overlap = CHUNK_OVERLAP
        self.top_k = TOP_K
        self.embedding_model = EMBEDDING_MODEL

    def get_vector_store_path(self, video_id : str) -> str:
        return str(get_faiss_directory(video_id))


# Global configuration instance
rag_config = RAGConfig()





