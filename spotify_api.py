import requests
from config import CLIENT_ID, CLIENT_SECRET
import base64

# Access Token 발급
def get_spotify_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    auth_data = {"grant_type": "client_credentials"}
    response = requests.post(auth_url, headers=auth_headers, data=auth_data)
    if response.status_code != 200:
        print("Failed to get token:", response.status_code, response.json())
        return None
    return response.json()["access_token"]

# 중복 제거
def remove_duplicates(artists):
    seen = set()
    unique_artists = []
    for artist in artists:
        if artist["id"] not in seen:
            unique_artists.append(artist)
            seen.add(artist["id"])
    return unique_artists

# 팔로워 수 하한선 필터링
def filter_by_min_followers(artists, min_followers=100000):
    return [artist for artist in artists if artist["followers"]["total"] >= min_followers]

def fetch_artists_with_min_followers(access_token, min_followers=100000, min_count=200):
    """하한선을 적용해 최소 min_count 아티스트를 확보"""
    queries = ['genre:"k-pop"', 'boy band', 'girl group']
    all_artists = []
    offset = 0
    limit = 50

    for query in queries:
        while len(all_artists) < min_count:
            url = "https://api.spotify.com/v1/search"
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {
                "q": query,
                "type": "artist",
                "limit": limit,
                "offset": offset
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                print(f"API request failed: {response.status_code}", response.json())
                break

            data = response.json()
            if "artists" not in data or not data["artists"]["items"]:
                print("No more artists found for query:", query)
                break

            # 가져온 데이터에서 하한선 필터링
            filtered_artists = filter_by_min_followers(data["artists"]["items"], min_followers)
            all_artists.extend(filtered_artists)

            # 중복 제거
            all_artists = remove_duplicates(all_artists)

            # 다음 페이지로 이동
            offset += limit

            # Spotify API의 최대 1,000개 제한 확인
            if offset >= 1000:
                print("Reached Spotify API pagination limit for query:", query)
                break

    return all_artists

def fetch_artist_followers(access_token, artist_id):
    """
    Spotify 아티스트 팔로워 수 가져오기
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch followers for {artist_id}: {response.status_code}")
        return None
    data = response.json()
    return data.get("followers", {}).get("total")
