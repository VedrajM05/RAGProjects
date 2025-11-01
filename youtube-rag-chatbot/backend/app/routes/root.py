from fastapi import APIRouter
import datetime


router = APIRouter(tags=["root"])

@router.get("/")
def root():
    return{"message" : "Welcome to Youtube RAG Chatbot"}