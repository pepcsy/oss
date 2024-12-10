from spotify_api import get_spotify_token, fetch_artists_with_min_followers
from db_manager import (
    initialize_database, save_artist_to_db, save_social_media_to_db, update_artist_social_id
)
from social_links_mapper import get_social_links_from_naver, extract_username

def main():
    # Step 1: 데이터베이스 초기화
    initialize_database()

    # Step 2: Spotify Access Token 발급
    access_token = get_spotify_token()
    if not access_token:
        print("Access Token 발급 실패")
        return

    # Step 3: Spotify 아티스트 데이터 수집 및 저장
    print("팔로워 수 하한선을 적용한 아티스트 검색 시작...")
    artists = fetch_artists_with_min_followers(access_token, min_followers=100000, min_count=200)

    print(f"총 {len(artists)}명의 아티스트 데이터 저장 중...")
    for artist in artists:
        save_artist_to_db({
            "name": artist["name"],
            "id": artist["id"],
            "genres": artist.get("genres", []),
            "followers": artist["followers"]["total"]
        })

    # Step 4: 소셜 링크 검색 및 저장
    print("소셜 링크 검색 및 데이터베이스 업데이트 시작...")
    for artist in artists:
        artist_name = artist["name"]
        print(f"{artist_name}의 소셜 링크를 네이버에서 검색 중...")
        social_links = get_social_links_from_naver(artist_name)

        # 소셜 미디어 정보 저장
        social_id = save_social_media_to_db(social_links)
        update_artist_social_id(artist_name, social_id)

        # 계정명 추출 (API 호출용)
        twitter_username = extract_username(social_links.get("twitter"), "twitter")
        instagram_username = extract_username(social_links.get("instagram"), "instagram")
        youtube_channel_id = extract_username(social_links.get("youtube"), "youtube")

        print(f"Extracted Usernames: Twitter: {twitter_username}, Instagram: {instagram_username}, YouTube: {youtube_channel_id}")

    print("소셜 링크 및 팔로워 정보 준비 완료!")

if __name__ == "__main__":
    main()
