from youtube_transcript_api  import YouTubeTranscriptApi, TranscriptsDisabled

start_word = "?v="
end_word = "&list="


video_url = "https://www.youtube.com/watch?v=IIvORO248Zs"
# video_url = "https://www.youtube.com/watch?v=2GV_ouHBw30&list=PLKnIA16_RmvbYFaaeLY28cWeqV-3vADST&index=1&t=597s"


api = YouTubeTranscriptApi()
# transcript_list = api.list(video_id = video_id)
# print(transcript_list)

def fetch_video_id_from_url(video_url : str) -> str:
    """
    Extracts video id if a user inputs a single video
    
    Args:
        playlisvideo_url : url of the single video
    
    Returns:
        video id of video from playlist
    """
    if "&index=" in video_url and "&list=" in video_url:
        print("Getting video id from Playlist")
        video_id = extract_video_id_from_playlist(video_url,start_word, end_word)

    else :
        print("Getting video id from the video url")
        video_id = video_url.split('?v=')
        print(video_id[1])
    
    return video_id

def extract_video_id_from_playlist(playlist_url, start_word, end_word) -> str:
    """
    Extracts video id if a user inputs a video from playlist
    
    Args:
        playlist_url: url of the video from playlist
        start_word: start word in the url Eg : '?v='
        end_word : end word in the url Eg : &list=
    
    Returns:
        video id of video from playlist
    """
    start_index = playlist_url.find(start_word)
    print(start_index)
    if start_index == -1:
        return None
    
    #  moves the starting position past the actual start word
    start_index += len(start_word)

    end_index = playlist_url.find(end_word, start_index)
    print(end_index)
    if end_index == -1:
        return None

    return playlist_url[start_index:end_index].strip()


print(fetch_video_id_from_url(video_url=video_url))


