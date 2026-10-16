'''
- Last.fm에서 곡에 붙은 tag를 가져오는 기능 작성
- MusicBrainz에서 확인한 곡의 탐색 단서를 보강
'''

import os       # .env에서 Last.fm API 키를 읽어오기 위해 사용
import requests # last.fm에 Http 요청을 보내기 위해 사용
from dotenv import load_dotenv # .env 설정을 환경변수로 불러오기 위해 사용

# .env 설정을 현재 python 프로그램에서 읽게 불러옴
load_dotenv()

# Last.fm 요청에 사용할 API 키를 환경변수에서 가져옴
LASTFM_API_KEY = os.environ["LASTFM_API_KEY"]

# Last.fm API 요청을 보낼 공통 주소
LASTFM_API_URL = "https://ws.audioscrobbler.com/2.0/"

# artist와 곡 제목으로 Last.fm의 태그 정보 요청
def fetch_track_top_tags(artist: str, track: str) -> dict:
    # Last.fm에 전달할 요청 조건 생성
    params = {
        "method" : "track.getTopTags",
        "artist" : artist,
        "track"  : track,
        "api_key": LASTFM_API_KEY,
        "format" : "json"
    }

    # 요청을 보내고, 요청 실패시 오류를 알림
    response = requests.get(LASTFM_API_URL, params = params, timeout = 10)
    response.raise_for_status()

    # 받은 JSON을 Python 딕셔너리로 변환해 반환
    data =  response.json()

    # Last.fm은 Http 요청이 성공해도 JSON 안에 API 오류를 담을 수 있음
    if "error" in data:
        raise RuntimeError(
            f"Last.fm API 오류 ({data["error"]}: {data.get("message", "알 수 없는 오류")})"
        )

    return data

# Last.fm 응답에서 tag 이름들을 목록으로 추출.
def extract_tag_names(data: str) -> list[str]:
    # 응답의 toptags -> tag 부분을 가져옴. tag가 없으면 빈 목록 사용
    tag_items = data.get("toptags", {}).get("tag", [])
    names = []

    # 각 tag의 이름만 목록에 담음
    for tag in tag_items:
        name = tag.get("name")
        if name:
            names.append(name)

    return names

# 이 파일을 직접 실행할 때만 테스트 수행
if __name__ == "__main__":
    # M83의 Midnight City 태그 정보 요청
    data = fetch_track_top_tags("M83", "Midnight City")

    # 원본 응답에서 태그 이름만 꺼냄
    tags = extract_tag_names(data)

    # 상위 10개 내용만 출력
    print("tag 수: ", len(tags))
    print("상위 태그: ", tags[ :10])

    # 태그가 없는 정상 응답을 가정해 추출 함수 확인
    empty_response = {"toptags": {"tags": []}}
    print("태그 없는 응답: ", extract_tag_names(empty_response))