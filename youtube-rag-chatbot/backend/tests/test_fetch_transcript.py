from backend.app.services.fetch_transcript import fetch_video_id_from_url, extract_video_id_from_playlist, fetch_transcript_from_video, get_text_from_raw_transcript


class FakeSnippet:
    def __init__(self, text : str):
        self.text = text

def test_fetch_video_id_from_url():
    # Arrange 
    url = "https://www.youtube.com/watch?v=zwUSZD3t_BU"

    # Act - call the function
    video_id = fetch_video_id_from_url(url)

    # Assert : check results
    assert video_id ==  "zwUSZD3t_BU"



def test_fetch_video_id_from_url_if_condition():
    # Arrange 
    video_url = "https://www.youtube.com/watch?v=pSVk-5WemQ0&list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0"

    # Act - call the function
    video_id = fetch_video_id_from_url(video_url)

    # Assert : check results
    assert video_id ==  "pSVk-5WemQ0"


def test_fetch_video_id_from_url_invalid_url():
    # Arrange 
    video_url = "https://www.youtube.com/watch?v1=zwUSZD3t_BU"

    # Act - call the function
    video_id = fetch_video_id_from_url(video_url)

    # Assert : check results
    assert video_id ==  None


def test_extract_video_id_from_playlist_positive():
     # Arrange 
    start_word = "?v="
    end_word = "&list="
    video_url = "https://www.youtube.com/watch?v=2GV_ouHBw30&list=PLKnIA16_RmvbYFaaeLY28cWeqV-3vADST&index=1&t=597s"

    # Act - call the function
    video_id = extract_video_id_from_playlist(video_url, start_word, end_word)

    # Assert : check results
    assert video_id ==  "2GV_ouHBw30"

def test_extract_video_id_from_playlist_negative():
     # Arrange 
    start_word = ""
    end_word = "&list="
    video_url = "https://www.youtube.com/watch?v=2GV_ouHBw30&list=PLKnIA16_RmvbYFaaeLY28cWeqV-3vADST&index=1&t=597s"

    # Act - call the function
    video_id = extract_video_id_from_playlist(video_url, start_word, end_word)

    # Assert : check results
    assert video_id !=  "2GV_ouHBw30"


def test_fetch_transcript_from_video_positive():
     # Arrange 
    video_id = "zwUSZD3t_BU"
    preferred_language = 'en'
    
    # Act - call the function
    transcript_text = fetch_transcript_from_video(video_id, preferred_language)

    # Assert : check results
    assert transcript_text != None

def test_fetch_transcript_from_video_negative():
     # Arrange 
    video_id = "zwUSZD3t_BU"
    preferred_language = 'hi'
    
    # Act - call the function
    transcript_text = fetch_transcript_from_video(video_id, preferred_language)

    # Assert : check results
    assert transcript_text == None


def test_get_text_from_raw_transcript_transcript_null():
     # Arrange 
    raw_transcript = ""
    
    # Act - call the function
    transcript_text = get_text_from_raw_transcript(raw_transcript)

    # Assert : check results
    assert transcript_text == ''

def test_get_text_from_raw_transcript_transcript_join():
     # Arrange 
    raw_transcript = [
        FakeSnippet("Hello"),
        FakeSnippet("from"),
        FakeSnippet("Youtube"),
    ]
    
    # Act - call the function
    transcript_text = get_text_from_raw_transcript(raw_transcript)

    # Assert : check results
    assert transcript_text == 'Hello from Youtube'

def test_get_text_from_raw_transcript_transcript_music():
     # Arrange 
    raw_transcript = [
        FakeSnippet("music"),
    ]
    
    # Act - call the function
    transcript_text = get_text_from_raw_transcript(raw_transcript)

    # Assert : check results
    assert transcript_text == ''

def test_get_text_from_raw_transcript_transcript_null():
     # Arrange 
    raw_transcript = [
        FakeSnippet(""),
    ]
    
    # Act - call the function
    transcript_text = get_text_from_raw_transcript(raw_transcript)

    # Assert : check results
    assert transcript_text == ''




# pytest --cov=backend --cov-report=html
# pytest --cov=backend --cov-report=term-missing




