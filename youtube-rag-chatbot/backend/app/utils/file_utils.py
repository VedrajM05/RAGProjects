import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


def ensure_video_directory(video_id : str) -> Path:
    """
    Create directory for video data if it doesn't exist
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Path to the video directory
    """
    video_directory = Path("app/data") / video_id

    #Create directory and parent if it doesnt exist
    video_directory.mkdir(parents=True)

    return video_directory

def save_transcript(video_id : str, final_transcript : str)-> str:
    """
    Save processed transcript text to backend/app/data/<video_id>/transcript.json
    
    Args:
        video_id: YouTube video ID
        transcript_text: Final processed transcript as string
        
    Returns:
        Path where the transcript was saved
    """
    # Ensure directory exists
    video_dir = ensure_video_directory(video_id)

    # Define transcript file path
    transcript_path = video_dir/"transcript.json"

    # Save transcript as json
    transcript_data = {
        "video_id" : video_id,
        "transcript" : final_transcript
    }

    with open(transcript_path, 'w', encoding='utf-8') as f:
        json.dump(transcript_data, f, indent=2, ensure_ascii=False)

    print(f"Transcript saved to {transcript_path}")
    return str(transcript_path)