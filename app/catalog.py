'''
- data/sample_tracks.json에서 샘플 곡 목록을 읽어옴
- JSON 데이터를 Track 객체로 바꿔 검색 기능에 전달함
'''
# JSON 파일의 내용을 Python의 목록, 딕셔너리로 읽어옴
import json
# 운영체제에 맞게 파일 경로를 다룸
from pathlib import Path
# 읽어온 곡 데이터를 Track 객체로 만들기 위해 가져옴
from app.models import Track

# 현재 파일의 위치 기준으로 프로젝트 루트 찾기
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# 프로젝트 루트 아래 샘플 데이터 파일 경로를 만듬
DATA_FILE = PROJECT_ROOT/"data"/"sample_tracks.json"

# Sample 파일을 읽어 Track 객체들의 목록으로 돌려줌
def load_tracks() -> list[Track]:
    # UTF-8 형식으로 JSON 파일을 열고, 사용이 끝나면 자동으로 닫음
    with DATA_FILE.open(encoding = "utf-8") as file:
        # JSON을 python 목록과 딕셔너리로 변환
        rows = json.load(file)

        # 변환한 Track 객체를 담을 빈 목록 생성
        tracks: list[Track] = []

        # JSON에서 읽은 곡 딕셔너리를 하나씩 처리
        for row in rows:
            track = Track(
                title = row["title"],
                artist = row["artist"],
                tags = row["tags"]
            )
            tracks.append(track)

        # 모든 곡을 변환한 뒤 목록 반환
        return tracks