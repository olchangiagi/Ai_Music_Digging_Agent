'''
- MusicBrainz에서 실제 곡 정보를 가져오는 기능 작성
- 외부 API 호출 코드를 샘플 JSON 로딩 코드와 분리
'''

import requests                  # MusicBrainz 서버에 HTTP 요청을 보내기 위해 사용
import os                        # 환경변수에서 user-Agent를 읽기 위해 사용
from dotenv import load_dotenv   # .env 내용을 환경변수로 불러오기 위해 사용
from app.models import Track     # 외부 응답을 프로젝트 공통 곡 형태로 변형하기 위해 사용

# .env를 읽은 뒤 MusicBrainz 요청에 사용할 프로그램 식별 정보를 가져옴
load_dotenv()
USER_AGENT = os.environ["MUSICBRAINZ_USER_AGENT"]

# MusicBrainz에서 곡의 녹음 정보(Recording)를 검색할 API 주소
RECORDING_SEARCH_URL = "https://musicbrainz.org/ws/2/recording/"

# 검색어를 입력받아 MusicBrainz의 곡 검색 조건 준비
def search_recordings(query: str) -> dict:
    # 서버에 전달할 검색어, 응답 형식, 결과 개수
    params = {
        "query" : query,
        "fmt"   : "json",
        "limit" : 5
    }

    # 검색 조건과 프로그램 식별 정보를 담아 요청
    response = requests.get(
        RECORDING_SEARCH_URL,
        params  = params,
        headers = {"User-Agent" : USER_AGENT},
        timeout = 10
    )

    # 요청이 실패했다면 오류를 알리고, 성공했다면 JSON 반환
    response.raise_for_status()
    return response.json()

# MusicBrainz recording ID로 특정 recording 하나를 조회
def get_recording_by_id(recording_id: str) -> dict:
    # 검색 주소 뒤에 ID를 붙이면 해당 recording 조회 주소
    url = f"{RECORDING_SEARCH_URL}{recording_id}"

    # JSON 형식으로 요청하고 HTTP 오류 확인
    response = requests.get(
        url,
        params = {"fmt": "json", "inc": "artist-credits"},
        headers = {"User-Agent": USER_AGENT},
        timeout = 10
    )
    response.raise_for_status()

    return response.json()

# MusicBrainz의 녹음 정보 한 건을 Track 객체로 변환
def recording_to_track(recording: dict) -> Track:
    # 첫 번째 표기 artist 이름 사용
    artist = recording["artist-credit"][0]["artist"]["name"]

    return Track(
        title   = recording["title"],
        artist  = artist,
        tags    = [],
        musicbrainz_id = recording["id"],
        disambiguation = recording.get("disambiguation") or None
    )

# 이 파일을 직접 실행할 때만 MusicBrainz 검색을 한 번 시험
if __name__ == "__main__":
    result = search_recordings('recording:"Midnight City" AND artist:"M83"')

    # 반환된 최대 5개 결과에서 곡 제목과 고유 ID 확인
    print("받은 곡 수: ", len(result["recordings"]))
    for recording in result["recordings"]:
        # 연결된 발매 정보 중 처음 3개의 제목 확인
        releases = recording.get("releases", [])
        release_titles = [release["title"] for release in releases[:3]]
        # artist-credit 목록의 첫 번째 아티스트 이름을 꺼냄
        artist = recording["artist-credit"][0]["artist"]["name"]
        print(recording["title"], "-", artist, 
              "| 길이(ms): ", recording.get("length"),
              "| 첫 발매: ", recording.get("first-release-date"),
              "| 설명: ", recording.get("disambiguation", "없음"),
              "| 발매: ", release_titles,
              "| ID: ", recording["id"],
              "| 검색 점수: ", recording.get("score")
        )

    if result["recordings"]:
        track = recording_to_track(result["recordings"][0])
        print("변환된 Track: ", track)

    # 설명(disambiguation)이 있는 녹음 하나를 찾아 변환 결과 확인
    for recording in result["recordings"]:
        if recording.get("disambiguation"):
            print("설명 있는 Track: ", recording_to_track(recording))
            break
