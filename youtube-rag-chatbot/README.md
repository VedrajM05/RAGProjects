# YouTube RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that processes YouTube videos and answers questions about their content.

## Backend Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation & Setup

    1. **Navigate to the backend directory**
    cd backend

    2. Create and activate virtual environment
    python -m venv .venv
    .venv\Scripts\activate

    3. Install dependencies
    pip install -r requirements.txt

    4. Run the FastAPI server
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

    5. Access the application
    API: http://127.0.0.1:8000
    API Docs: http://127.0.0.1:8000/docs

