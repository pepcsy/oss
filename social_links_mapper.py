import requests
from bs4 import BeautifulSoup

def get_social_links_from_naver(artist_name):
    """
    네이버 검색 결과에서 아티스트의 유튜브, 트위터, 인스타그램 링크를 가져옵니다.
    """
    search_url = f"https://search.naver.com/search.naver?query={artist_name}"
    try:
        response = requests.get(search_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            social_links = {"twitter": None, "instagram": None, "youtube": None}

            # 프로필 섹션에서 링크 추출
            profile_section = soup.select_one("div.cm_content_wrap > div.cm_content_area._cm_content_area_profile")
            if profile_section:
                for link in profile_section.find_all("a", href=True):
                    href = link["href"]
                    if "twitter.com" in href and not social_links["twitter"]:
                        social_links["twitter"] = href
                    elif "instagram.com" in href and not social_links["instagram"]:
                        social_links["instagram"] = href
                    elif "youtube.com" in href and not social_links["youtube"]:
                        social_links["youtube"] = href

            return social_links

        else:
            print(f"네이버 검색 요청 실패: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"네이버 크롤링 중 오류 발생: {e}")
    return {"twitter": None, "instagram": None, "youtube": None}

def extract_username(url, platform):
    """
    소셜 미디어 링크에서 계정명 추출
    """
    if not url:  # URL이 None일 경우
        return None

    if platform == "twitter" and "twitter.com" in url:
        return url.split("/")[-1]
    elif platform == "instagram" and "instagram.com" in url:
        return url.split("/")[-1]
    elif platform == "youtube" and "youtube.com" in url:
        # 유튜브 채널 ID 추출
        if "channel/" in url:
            return url.split("channel/")[-1]
        elif "user/" in url:
            return url.split("user/")[-1]
    return None
