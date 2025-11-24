"""
Map-Reduce summarization for long transcripts
"""

from app.services.text_splitter_service import split_transcript
from app.utils.file_utils import load_transcript_text
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

class SummaryService:
    def __init__(self):
        self.llm = None
        self._setup_llm()
    
    def _setup_llm(self):
        """Initialize LLM for summarization"""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.1,
                    openai_api_key=api_key
                )
                print("Summary service LLM initialized")
        except Exception as e:
            print(f"Summary LLM setup failed: {e}")
    
    def generate_summary(self, video_id: str, question: str) -> str:
        """
        Generate 5-bullet summary using map-reduce approach
        """
        print(f"generate_summary")
        try:
            # Load transcript
            transcript_text = load_transcript_text(video_id)
            if not transcript_text:
                return "No transcript available for summary."
            
            print(f"Processing transcript ({len(transcript_text)} chars) for summary...")
            
            # Map Step: Split and create chunk summaries
            chunk_summaries = self._process_chunks(transcript_text, video_id)
            
            if not chunk_summaries:
                return "Could not generate summary from transcript."
            
            # Reduce Step: Merge into final summary
            final_summary = self._create_final_summary(chunk_summaries, question)
            
            return final_summary
            
        except Exception as e:
            print(f"Summary generation failed: {e}")
            return f"Error generating summary: {str(e)}"
    
    def _process_chunks(self, transcript_text: str, video_id: str) -> list[str]:
        """
        Process transcript chunks and generate summaries
        """
        print(f"_process_chunks")
        chunks = split_transcript(transcript_text, video_id)
        print(f"Split into {len(chunks)} chunks for summarization")
        
        chunk_summaries = []
        
        # Process first 8 chunks max (for efficiency)
        for i, chunk in enumerate(chunks[:8]):
            try:
                summary = self._summarize_chunk(chunk['text'])
                if summary and summary.strip():
                    chunk_summaries.append(summary)
                    print(f"Chunk {i+1} summarized")
            except Exception as e:
                print(f"Failed to summarize chunk {i+1}: {e}")
        
        return chunk_summaries
    
    def _summarize_chunk(self, chunk_text: str) -> str:
        """
        Summarize a single chunk using LLM
        """
        if not self.llm or not chunk_text.strip():
            return ""
        
        try:
            messages = [
                SystemMessage(content="""You are a concise summarizer. 
                Summarize this video transcript chunk in 1-2 sentences.
                Focus on the main ideas and key information."""),
                HumanMessage(content=chunk_text[:2000])  # Limit chunk size
            ]
            
            response = self.llm.invoke(messages)
            return response.content.strip()
            
        except Exception as e:
            print(f"Chunk summarization failed: {e}")
            return ""
    
    def _create_final_summary(self, chunk_summaries: list[str], question: str) -> str:
        """
        Create final summary from chunk summaries
        """
        if not chunk_summaries:
            return "No content available for summary."
        
        # Try LLM-based summary first
        if self.llm:
            try:
                combined_summaries = "\n\n".join(chunk_summaries)
                
                messages = [
                    SystemMessage(content="""You are creating a final video summary.
                    Create exactly 5 bullet points that cover the main topics discussed.
                    Each bullet should be concise and informative.
                    Format with • bullets and ensure exactly 5 points."""),
                    HumanMessage(content=f"""Original question: {question}
                    
                    Chunk summaries to combine:
                    {combined_summaries}
                    
                    Create exactly 5 bullet points:""")
                ]
                
                response = self.llm.invoke(messages)
                return response.content.strip()
                
            except Exception as e:
                print(f"Final summary reduction failed: {e}")
        
        # Fallback: simple bullet points
        return self._create_fallback_bullets(chunk_summaries)
    
    def _create_fallback_bullets(self, chunk_summaries: list[str]) -> str:
        """
        Create fallback bullet points from chunk summaries
        """
        unique_summaries = list(set([s for s in chunk_summaries if s.strip()]))
        top_points = unique_summaries[:5]
        
        if not top_points:
            return """• The video covers various topics discussed by the speaker.
• Multiple points are addressed throughout the content.
• The speaker shares insights on different subjects.
• Key information is presented in the video.
• Various concepts are explained in detail."""
        
        return "\n".join([f"• {point}" for point in top_points if point])

# Global instance
summary_service = SummaryService()

# Convenience function
def generate_summary1(video_id: str, question: str) -> str:
    """Generate summary for a video"""
    print(f"Convenience function : generate_summary1")
    return summary_service.generate_summary(video_id, question)