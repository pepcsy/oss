from spotify_api import get_spotify_token, fetch_artists_with_min_followers, fetch_artist_followers
from db_manager import (
    initialize_database, save_artist_to_db, save_social_media_to_db, update_artist_social_id, update_followers_in_db, save_daily_followers
)
from social_links_mapper import get_social_links_from_naver, extract_username
import sqlite3
import sys

from youtube_api import get_youtube_subscriber_count

def main():
    print("[INFO] Initializing database...")
    # Step 1: 데이터베이스 초기화
    initialize_database()
    print("[INFO] Database initialized.")

    print("[INFO] Requesting Spotify Access Token...")
    # Step 2: Spotify Access Token 발급
    access_token = get_spotify_token()
    if not access_token:
        print("[ERROR] Access Token 발급 실패")
        return

    print("[INFO] Spotify Access Token obtained.")

    # Step 3: Spotify 아티스트 데이터 수집 및 저장
    print("[INFO] Fetching artists with minimum followers...")
    artists = fetch_artists_with_min_followers(access_token, min_followers=100000, min_count=200)

    print(f"[INFO] {len(artists)} artists fetched. Saving to database...")
    for artist in artists:
        print(f"[DEBUG] Saving artist: {artist['name']} ({artist['id']})")
        save_artist_to_db({
            "name": artist["name"],
            "id": artist["id"],
            "genres": artist.get("genres", []),
            "followers": artist["followers"]["total"]
        })

    print("[INFO] Artist data saved.")

    # Step 4: 소셜 링크 검색 및 저장
    print("[INFO] Fetching social media links for artists...")
    for artist in artists:
        artist_name = artist["name"]
        print(f"[DEBUG] Searching social links for: {artist_name}")
        social_links = get_social_links_from_naver(artist_name)

        if social_links:
            print(f"[DEBUG] Social links found for {artist_name}: {social_links}")
            social_id = save_social_media_to_db(social_links)
            update_artist_social_id(artist_name, social_id)

            twitter_username = extract_username(social_links.get("twitter"), "twitter")
            instagram_username = extract_username(social_links.get("instagram"), "instagram")
            youtube_channel_id = extract_username(social_links.get("youtube"), "youtube")

            print(f"[INFO] Usernames extracted for {artist_name}: Twitter={twitter_username}, Instagram={instagram_username}, YouTube={youtube_channel_id}")
        else:
            print(f"[WARNING] No social links found for {artist_name}.")

    print("[INFO] Social media data saved and updated.")

def update_followers():
    print("[INFO] Updating follower counts...")
    # Spotify Access Token 발급
    access_token = get_spotify_token()
    if not access_token:
        print("[ERROR] Spotify Access Token 발급 실패")
        return

    # DB에서 아티스트 이름과 Spotify ID 불러오기
    conn = sqlite3.connect("data/kpop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, spotify_id FROM artists")
    artists = cursor.fetchall()
    conn.close()

    # Spotify 팔로워 업데이트
    for artist_id, name, spotify_id in artists:
        print(f"[DEBUG] Fetching followers for {name} (Spotify ID: {spotify_id})")
        followers = fetch_artist_followers(access_token, spotify_id)
        if followers is not None:
            update_followers_in_db(name, "spotify", followers)
            save_daily_followers(artist_id, "spotify", followers)
            print(f"[INFO] {name}: Spotify followers updated to {followers}")

def update_youtube_subscribers():
    print("[INFO] Updating YouTube subscribers...")

    # DB에서 아티스트 이름과 YouTube 채널 URL 불러오기
    conn = sqlite3.connect("data/kpop.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, a.name, sm.youtube
        FROM artists a
        JOIN social_media sm ON a.social_id = sm.id
        WHERE sm.youtube IS NOT NULL
    """)
    youtube_channels = cursor.fetchall()
    conn.close()

    # YouTube 구독자 수 업데이트
    for artist_id, name, youtube_url in youtube_channels:
        # YouTube ID 추출
        channel_id = extract_username(youtube_url, "youtube")
        if not channel_id:
            print(f"[WARNING] Invalid YouTube URL for {name}: {youtube_url}")
            continue

        print(f"[DEBUG] Fetching subscribers for {name} (YouTube ID: {channel_id})")
        subscribers = get_youtube_subscriber_count(channel_id)
        if subscribers is not None:
            update_followers_in_db(name, "youtube", subscribers)
            save_daily_followers(artist_id, "youtube", subscribers)
            print(f"[INFO] {name}: YouTube subscribers updated to {subscribers}")
        else:
            print(f"[WARNING] No data found for YouTube channel ID: {channel_id}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "update":
            update_followers()
        elif sys.argv[1] == "youtube":
            update_youtube_subscribers()
    else:
        main()
