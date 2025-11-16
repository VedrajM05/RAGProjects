import json
from pathlib import Path
import shutil
from app.core.config import config


def ensure_video_directory(video_id : str) -> Path:
    """
    Create directory for video data if it doesn't exist
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Path to the video directory
    """
    video_directory = Path(config.data_folder) / video_id
    
    #Delete directory if it exists and recreate
    if not video_directory.exists():
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
    transcript_path = video_dir/config.transcript_dot_json

    # Save transcript as json
    transcript_data = {
        "video_id" : video_id,
        "transcript" : final_transcript
    }

    with open(transcript_path, 'w', encoding='utf-8') as f:
        json.dump(transcript_data, f, indent=2, ensure_ascii=False)

    print(f"Transcript saved to {transcript_path}")
    return str(transcript_path)



def transcript_exists(video_id : str) -> bool:
    """
    Check if a transcript exists for a video based on video id
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        True/False indicating if transcript exists or not
    """
    transcript_path = Path(config.data_folder) / video_id / config.transcript_dot_json
    return transcript_path.exists()

def load_transcript_text(video_id : str) -> str:
    """
    Load transcript text from backend/app/data/<video_id>/transcript.json
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Transcript text as string or empty string if not found
    """
    transcript_path = Path(config.data_folder) / video_id / config.transcript_dot_json
    print(transcript_path)
    if not transcript_path.exists():
        print("transcript path not found")
        return ""
    
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("transcript", "")
    
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading transcript for video_id : {video_id} : {e}")
        return ""