"""
Response Service for generating answers using LLM
"""

class ResponseService():
    def __init__(self):
        # Initialize retriever, embeddings, model pipeline
        pass


    def build_context(self, video_id : str, query : str, top_k : int = 3)-> list[dict]:
        """
        Retrieve top relevant chunks for the query
        Input: Video ID, user query
        Output: List of top chunks with metadata
        """

        # Connect to retriever, get most relevant segments
        pass


    def build_prompt(self, context_chunks : list[dict], query : str)-> str:
        """
        Build prompt using template and context
        Input: Context chunks + user query  
        Output: Formatted prompt string
        """

        # Fill {context} and {query} placeholder from markdown template  
        pass


    def generate_llm_response(self, prompt : str)-> str:
        """
        Send prompt to LLM and get response
        
        Input: Prompt string
        Output: LLM response text
        """

        # Invoke model and retreive output  
        pass


    def format_response(self, llm_output : str, context_chunks : list[dict])-> dict:
        """
        Format final response with answer and sources
        
        Input: Model output + context metadata
        Output: Structured response dict
        """

        # Create {"answer" : ..., "sources" : [...]} format 
        pass

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



    