from fastapi import FastAPI
from app.core.config import config
from app.routes import health, process_video
from app.routes import ask_question

app = FastAPI(
    title = config.APP_NAME,
    version= config.VERSION 
)

# Wire the health router into the main app
app.include_router(health.router)

# Wire the process_video into the main app
app.include_router(process_video.router)

# Wire the ask question  into the main app
app.include_router(ask_question.router)


# Run from here
# PS C:\RAGProjects\youtube-rag-chatbot\backend> uvicorn app.main:app --reload --port 8000

#docs
# http://localhost:8000/docs