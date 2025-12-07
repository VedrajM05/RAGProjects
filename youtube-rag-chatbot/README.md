# 🎬 YouTube RAG Chatbot
AI-powered Assistant to Analyze and Chat with Any YouTube Video

This project is an end-to-end Retrieval-Augmented Generation (RAG) system built using FastAPI, Angular, LangChain, OpenAI, FAISS and Docker.

Paste a YouTube URL → System extracts the transcript → Builds vector embeddings → Answers questions → Generates summaries → Detects user intent (summarize / ask / explain / insights).

🚀 Features
🔹 Full RAG Pipeline

Extracts YouTube transcripts

Splits transcript into semantically meaningful chunks

Generates embeddings using Sentence Transformers

Stores and retrieves vectors using FAISS

Answers user queries grounded in video content

🔹 Two AI Engines

QA Engine → Detailed grounded answers

Summarization Engine → 5-point concise summaries

Intent detection automatically routes to the right engine

🔹 Modern Frontend

Angular UI

Clean, responsive Bootstrap styling

Real-time chat-style interface

“Process Video” → “Ask Questions” workflow

🔹 Production-Ready Backend

FastAPI server

Modular service architecture

Clean separation: Transcript → Chunking → Embeddings → Retrieval → LLM → Response formatting

🔹 DevOps & Deployment

Dockerized backend & frontend

Docker Compose multi-service deployment

GitHub Actions CI Pipeline

Backend tests (pytest + TestClient)

Angular unit tests

Lint + build verification

🔹 Testing

Unit tests for FastAPI

Unit tests for Angular

Mocked services for deterministic testing

🛠️ Tech Stack
Backend

Python 3.x

FastAPI

LangChain

FAISS

OpenAI GPT-4 models

yt_dlp (for transcript extraction)

Frontend

Angular

TypeScript

Bootstrap

RxJS

ML & AI

Sentence Transformer: all-MiniLM-L6-v2

Retrieval-Augmented Generation

Intent Classification Prompt

Summarization Map-Reduce logic

DevOps

Docker

Docker Compose

GitHub Actions (CI)


📁 Project Structure
/frontend
    /src
        /app
            components/
            services/
            models/
    Dockerfile

/backend
    app/
        api/
        services/
        utils/
        prompts/
        models/
    tests/
    Dockerfile

docker-compose.yml
README.md

🚀 Local Development Setup
1. Clone Repo
git clone <repo-url>
cd youtube-rag-chatbot

2. Run Backend + Frontend with Docker Compose
docker compose up --build


Backend → http://localhost:8000
Frontend → http://localhost:4200

🧪 Running Tests
Backend
cd backend
pytest

Frontend
cd frontend
ng test