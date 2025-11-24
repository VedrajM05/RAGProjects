"""
Intent detection for RAG routing - SUMMARY vs QA classification
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from app.rag_pipeline_config import LLM_MODEL_NAME5


class IntentService:
    def __init__(self):
        self.llm = None
        self.setup_OpenAI()

    def setup_OpenAI(self):
        """Initialize OpenAI client"""
        
        load_dotenv()

        API_KEY = os.getenv("OPENAI_API_KEY")
        if API_KEY : 
            self.llm = ChatOpenAI(
                model=LLM_MODEL_NAME5,
                api_key=API_KEY,
                # max_tokens = 10,
                # temperature = 0.1
            )
            print(f"API_KEY initialized") 
        else : 
            print(f"API_KEY not initialized, using fallback detection") 
    

    def detect_intent(self, question : str) -> str :
        """Classify user question as summary or QA question"""    
        openAI_intent = self.detect_with_OpenAI(question)
        if openAI_intent:
            return openAI_intent
        
        return self.detect_with_keywords(question)
    
    def detect_with_OpenAI(self, question : str) -> str :
        """Use OpenAI for intent classification"""
        if not self.llm:
            return None
        
        try:
            messages = [
                    SystemMessage(content="""You are intent classifier for youtube video questions.
                        Classify the user's question into exactly one of these 2 categories :
                        - Summary : User wants overall summary, main points, key takeaways
                        - QA : User asks about specific details, facts, explanations, timestamps
                        Respond with only 1 word : "SUMMARY" or "QA" 
                    """),
                    HumanMessage(content=question)
                ]
            response = self.llm.invoke(messages)
            
            intent = response.content.strip().upper()
            print("intent ", intent)
            if intent in ["SUMMARY" , "QA" ]:
                return intent
            else:
                print(f"OpenAI returned invalid intent : {intent}")
                return None
            
        
        except Exception as e:
            #traceback.print_exc()
            print(f"OpenAI intent detected failed : {e}")
            return None
        

    def detect_with_keywords(self, question : str) -> str :
        """Fallback keyword-based intent detection"""
        summary_keywords = [
            'summarize', 'summary', 'overview', 'main points', 'key takeaways',
            'what is this video about', 'what\'s this video about', 
            'explain this video', 'brief', 'recap', 'tl;dr', 'tl dr',
            'main ideas', 'key points', 'gist', 'high level', 'big picture'
        ]

        for keyword in summary_keywords:
            if keyword in question.lower():
                return "Summary"
            

        return "QA"
    
# Global instance 
intent_service = IntentService()


def detect_intent(question : str) -> str:
    return intent_service.detect_intent(question)