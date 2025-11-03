from youtube_transcript_api  import YouTubeTranscriptApi, TranscriptsDisabled

start_word = "?v="
end_word = "&list="

# video_url = "https://www.youtube.com/watch?v=pSVk-5WemQ0&list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0"
# video_url = "https://www.youtube.com/watch?v=IIvORO248Zs"
# video_url = "https://www.youtube.com/watch?v=2GV_ouHBw30&list=PLKnIA16_RmvbYFaaeLY28cWeqV-3vADST&index=1&t=597s"
video_url = ""
#======================================fetch_video_id_from_url======================================
def fetch_video_id_from_url(video_url : str) -> str:
    """
    Extracts video id if a user inputs a single video
    
    Args:
        playlisvideo_url : url of the single video
    
    Returns:
        video id of video from playlist
    """
    if "&list=" in video_url:
        print("Getting video id from Playlist")
        video_id = extract_video_id_from_playlist(video_url,start_word, end_word)
        return video_id

    else :
        print("Getting video id from the video url")
        if "?v=" in video_url:
            video_id = video_url.split('?v=')
            print("Video id found : ",video_id[1])
            return video_id[1]
        else:
            print("Invalid Video URL : ",video_url)
            return None

#======================================extract_video_id_from_playlist======================================
def extract_video_id_from_playlist(playlist_url, start_word, end_word) -> str:
    """
    Extracts video id if a user inputs a video from playlist
    
    Args:
        playlist_url: url of the video from playlist
        start_word: start word in the url Eg : '?v='
        end_word : end word in the url Eg : '&list='
    
    Returns:
        video id of video from playlist
    """
    start_index = playlist_url.find(start_word)
    #print(start_index)
    if start_index == -1:
        return None
    
    #  moves the starting position past the actual start word
    start_index += len(start_word)

    end_index = playlist_url.find(end_word, start_index)
    #print(end_index)
    if end_index == -1:
        return None
    video_id = playlist_url[start_index:end_index].strip()
    print("Video id found : ",video_id)
    return video_id


#======================================fetch_transcript_from_video======================================

def fetch_transcript_from_video(video_id : str, preferred_language = 'en') -> list[dict]:
    """
    Fetch raw transcript from youtube api based on video id and preferred language
    
    Args:
        video_id: youtube id of the video
        preferred_language: preferred transcript language Eg : 'en'
    
    Returns:
        list of dictionary of transcripts of entire video
    """
    api = YouTubeTranscriptApi()
    try:
        transcript_list = api.list(video_id = video_id)
        transcript = transcript_list.find_generated_transcript([preferred_language])
        transcript_raw = transcript.fetch()
        
        # print("Transcript : ",transcript_raw)
        # final_transcript = " ".join(chunk["text"] for chunk in transcript_raw)
        return transcript_raw

    except TranscriptsDisabled:
        print("No captions available for this video")

    except Exception as e:
        print(f"Exception : ",str(e))
        return None


#======================================get_text_from_raw_transcript======================================
# ignoring music segments.
def get_text_from_raw_transcript(raw_transcript : list[dict]) -> str:
    """
    Convert raw transcript into a single string
    
    Args:
        raw_transcript: raw transcript in list dictionary form with text, start time and durtion of each transcript
    
    Returns:
        final string from raw transcript for entire video
    """
    single_transcript = []
    for segment in raw_transcript:
        text = segment.text
        
        # Skip music indicators
        if text.lower() in ['music', '[music]']:
            continue
        # Skip empty text
        if not text:
            continue
        # combine all text parts into an array
        single_transcript.append(text)
    
    # Combine all parts with spaces    
    full_text = ' '.join(single_transcript)
    print(full_text)
    return full_text 


# videoId = fetch_video_id_from_url(video_url)
# if videoId:
#     raw_transcript = fetch_transcript_from_video(videoId)
#     if raw_transcript:
#         final_transcript = get_text_from_raw_transcript(raw_transcript)
