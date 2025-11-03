# backend/app/core/config.py

import os

class Config:
    APP_NAME = "Youtube RAG Chatbot"
    VERSION = "1.0.0"

    #API Keys
    hf_api_keys = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    #Transcript variables
    data_folder = "app/data"
    transcript_dot_json = "transcript.json"


# Global config instance
config = Config()