from backend.app.services.fetch_transcript import fetch_video_id_from_url

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

# pytest --cov=backend --cov-report=html



