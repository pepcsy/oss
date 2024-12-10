'''from bs4 import BeautifulSoup
import requests

def get_twitter_handle(artist_name):
    """
    Wikipedia 페이지를 크롤링하여 트위터 계정을 가져옵니다.
    """
    # Wikipedia 페이지 URL 생성
    search_url = f"https://en.wikipedia.org/wiki/{artist_name.replace(' ', '_')}"
    try:
        response = requests.get(search_url, timeout=10)
        # HTTP 응답이 정상인지 확인
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # 모든 <a> 태그에서 href 속성 검색
            for link in soup.find_all("a", href=True):
                # 트위터 링크인지 확인
                if "twitter.com" in link["href"]:
                    return link["href"].split("/")[-1]  # 트위터 계정명 반환
        else:
            print(f"Wikipedia 페이지를 찾을 수 없습니다: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류 발생: {e}")
    return None
'''