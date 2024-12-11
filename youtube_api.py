import requests
from config import YOUTUBE_API_KEY

def get_youtube_subscriber_count(channel_id):
    """
    YouTube 채널 ID를 사용하여 구독자 수를 가져옴.
    """
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch YouTube data: {response.status_code}")
        print(response.json())  # 에러 메시지 출력
        return None

    data = response.json()
    if "items" in data and len(data["items"]) > 0:
        return int(data["items"][0]["statistics"]["subscriberCount"])
    else:
        print(f"[WARNING] No data found for YouTube channel ID: {channel_id}")
        return None
