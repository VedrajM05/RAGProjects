"""
Response Service for generating answers using LLM
"""

import os
import traceback

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from transformers import pipeline
from app.models.query_models import AskResponse
from app.services.retriever_service import get_retriever
from app.rag_pipeline_config import LLM_MODEL_NAME1, LLM_MODEL_NAME2, TOP_K
from dotenv import load_dotenv

class ResponseService():
    def __init__(self):
        # Initialize retriever, embeddings, model pipeline
        pass


    def build_context(self, video_id : str, query : str, top_k : int = TOP_K)-> list[dict]:
        """
        Retrieve top relevant chunks for the query
        
        Input: Video ID, user query
        Output: List of top chunks with metadata
        """

        # Connect to retriever, get most relevant segments
        retriever = get_retriever(video_id)
        chunks = retriever.retrieve(query, top_k= TOP_K)
        return chunks


    def build_prompt(self, context_chunks : list[dict], query : str)-> str:
        """
        Build prompt using template and context

        Input: Context chunks + user query  
        Output: Formatted prompt string
        """
        #Read prompt template file
        template_path = 'docs/prompts/video_rag_prompt.md'

        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
        else : 
            raise FileNotFoundError(f"Could not find prompt template file at path : {template_path}")
        

        # Format chunks : add numbering
        formatted_chunks = []
        for i,chunk in enumerate(context_chunks):
            formatted_chunks.append(f"Chunk {i + 1} : {chunk['text']}")

        
        context_text = "\n\n".join(formatted_chunks)
        
        # Fill {context} and {query} placeholder from markdown template
        prompt = template.replace("{context_chunks}", context_text)
        prompt = prompt.replace("{user_question}", query)

        # Return formatted prompt 
        return prompt


    def generate_llm_response(self, prompt : str)-> str:
        """
        Send prompt to LLM and get response
        
        Input: Prompt string
        Output: LLM response text
        """
        
        # Load environment variables from .env file
        load_dotenv()

        API_KEY = os.getenv("OPENAI_API_KEY")
        if not API_KEY : 
            return f"API_KEY not found in env variables"
        
        # Step 1: Create a pipeline : Hugging Face local/internet-accessible model, using the Transformers pipeline interface
        try:
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.2,
                api_key=API_KEY
            )
            # Invoke model and retreive output 
            response = llm.invoke([HumanMessage(content=prompt)])
            
            return response.content
        
        except Exception as e:
            #traceback.print_exc()
            return f"Exception : Error calling LLM {str(e)}"


    def format_response(self, llm_output : str, context_chunks : list[dict])-> dict:
        """
        Format final response with answer and sources
        
        Input: Model output + context metadata
        Output: Structured response dict
        """

        # Create {"answer" : ..., "sources" : [...]} format 
        json_output = llm_output.strip()
        if json_output.lower().startswith("answer:"):
            json_output = json_output[len("answer:"):].strip()

        return AskResponse(answer=json_output)

    def generate_answer(self, video_id: str, query : str)-> dict:
        """
        Orchestrator method: complete pipeline from query to answer
        
        Input: Video ID, user query
        Output: Structured response with answer and sources
        """

        # 1 Get relevant chunks 
        context_chunks = self.build_context(video_id, query)

        # 2 Build prompt
        prompt = self.build_prompt(context_chunks, query)

        # 3 Get LLM response
        llm_output = self.generate_llm_response(prompt)

        # 4 Format final response
        response = self.format_response(llm_output, context_chunks)

        return response
    

# Create global instance so that any one can access this service class
response_service = ResponseService()



    