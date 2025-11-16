from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import config
from app.routes import health, process_video
from app.routes import ask_question, chunk_transcript

app = FastAPI(
    title = config.APP_NAME,
    version= config.VERSION 
)

# @app.middleware("http")
# async def debug_cors(request : Request, call_next):
#     print(f"Incoming Request : {request.method}  {request.url}")
#     response = await call_next(request)
#     print(f"Response headers : {dict(response.headers)}")
#     return response


# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:4200"],
    allow_credentials = True,
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers = ["*"],
)


# Wire the health router into the main app
app.include_router(health.router)

# Wire the process_video into the main app
app.include_router(process_video.router)

# Wire the ask question  into the main app
app.include_router(ask_question.router)

# Wire the chunk_transcript  into the main app
app.include_router(chunk_transcript.router)

# Run from here
# PS C:\RAGProjects\youtube-rag-chatbot\backend> uvicorn app.main:app --reload --port 8000

#docs
# http://localhost:8000/docs