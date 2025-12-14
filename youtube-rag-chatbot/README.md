# 🎬 YouTube RAG Chatbot
### AI-Powered Assistant to Chat, Ask Questions & Summarize Any YouTube Video

An end-to-end **Retrieval-Augmented Generation (RAG)** application that allows users to paste a YouTube URL, automatically process the video transcript, and interact with the content through **Q&A and summarization**, powered by **LLMs, vector search, and modern MLOps practices**.

---

## ✨ Key Features

### 🧠 RAG Pipeline (End-to-End)
- YouTube transcript extraction
- Semantic chunking of transcripts
- Embedding generation using Sentence Transformers
- FAISS vector store for fast similarity search
- Context-aware retrieval for LLM grounding

### 🤖 Dual AI Engines
- **Q&A Engine** – factual, grounded answers from transcript
- **Summarization Engine** – map-reduce style summarization
- Intent detection routes user queries to the correct engine

### 💬 Modern Chat UI
- Angular frontend
- Responsive Bootstrap UI
- Chat-like conversation experience
- Supports multiple videos per session

### ⚙️ Production-Ready Backend
- FastAPI-based service architecture
- Modular services for transcript, embeddings, retrieval, and response generation
- Clear separation of concerns

### 🧪 Testing & CI
- Backend unit tests (pytest)
- Frontend unit tests (Angular)
- GitHub Actions CI pipeline validating:
  - Backend tests
  - Frontend tests
  - Build integrity

### 📦 DevOps & Deployment Ready
- Dockerized backend and frontend
- Docker Compose for local multi-service deployment
- CI ready for extension into full CD pipelines

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- LangChain
- FAISS
- OpenAI (GPT models)
- Sentence Transformers
- yt_dlp (transcript extraction)

### Frontend
- Angular
- TypeScript
- Bootstrap
- RxJS

### AI / ML
- Retrieval-Augmented Generation (RAG)
- Vector embeddings (`all-MiniLM-L6-v2`)
- Map-Reduce summarization
- Intent classification via LLM prompting

### DevOps
- Docker
- Docker Compose
- GitHub Actions (CI)

---

## 🧩 Architecture Overview

User
 └── Angular UI
       └── FastAPI Backend
             ├── Transcript Service
             ├── Chunking Service
             ├── Embedding Service
             ├── FAISS Vector Store
             ├── Retrieval Layer
             ├── Intent Detection
             └── LLM Response Engine



---

## 📁 Project Structure

youtube-rag-chatbot/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── prompts/
│   │   ├── models/
│   │   └── utils/
│   ├── tests/
│   └── Dockerfile
│
├── frontend/
│   ├── src/app/
│   └── Dockerfile
│
├── docker-compose.yml
├── .github/workflows/ci.yml
└── README.md



---

## 🚀 Getting Started (Local)

### 1️⃣ Clone Repository
```bash
git clone https://github.com/VedrajM05/RAGProjects.git
cd youtube-rag-chatbot

2️⃣ Run with Docker Compose
docker compose up --build

Frontend: http://localhost:4200
Backend: http://localhost:8000
API Docs: http://localhost:8000/docs

🧪 Running Tests
Backend
cd backend
pytest

Frontend
cd frontend/my-ui
ng test

🔮 Backlog / Future Enhancements

(Intentionally deferred to focus on core functionality)

Advanced semantic chunking strategies

Runnable-based LangChain refactors

PromptTemplate standardization

Chunk-reference cleanup in responses

Full observability (logging, metrics)

Kubernetes deployment

Advanced analytics & insights engine

👨‍💻 Author

Vedraj Mokashi
.NET & Angular Full-Stack Developer (7+ Years Experience)
Currently transitioning into AI / Machine Learning & LLM Engineering

📌 Professional Background

7+ years of experience building enterprise-grade web applications

Strong expertise in .NET, ASP.NET, Angular, SQL, REST APIs

Proven experience with production systems, scalability, and clean architecture

Actively transitioning into AI/ML, RAG systems, and LLM-based applications

📌 Current Focus Areas

Retrieval-Augmented Generation (RAG)

Large Language Models (LLMs)

LangChain & LangGraph (Agentic AI)

AI-powered backend systems with FastAPI

MLOps fundamentals (Docker, CI/CD, deployment)

Bridging traditional full-stack engineering with modern AI systems

⭐ Support

If you found this project useful or insightful, consider starring the repository ⭐
It helps support future work and open-source contributions.