'''
- data/sample_tracks.json에서 샘플 곡 목록을 읽어옴
- JSON 데이터를 Track 객체로 바꿔 검색 기능에 전달함
'''

import json                     # JSON 파일의 내용을 Python의 목록, 딕셔너리로 읽어옴
from pathlib import Path        # 운영체제에 맞게 파일 경로를 다룸
from app.models import Track    # 읽어온 곡 데이터를 Track 객체로 만들기 위해 가져옴
from dataclasses import asdict  # Track을 Json으로 쓸 딕셔너리로 변환

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

# 곡 한 개가 담긴 JSON 파일을 다시 Track 객체로 읽어옴
def load_track_from_json(path: Path) -> Track:
    # JSON 파일을 python 딕셔너리로 읽음
    with path.open(encoding = "utf-8") as file:
        row = json.load(file)

    # 딕셔너리의 키를 Track의 필드에 대응시켜 객체를 만듬
    return Track(**row)

# Track 한 개를 새 JSON 파일로 저장
def save_track_to_json(track: Track, path: Path) -> None:
    # "x" 모드는 기존 파일을 덮어쓰지 않음
    with path.open("x", encoding = "utf-8") as file:
        json.dump(asdict(track), file, ensure_ascii = False, indent = 2)

# 이 파일을 직접 실행할 때만 코드 실행
if __name__ == "__main__":
    saved_path = PROJECT_ROOT/"data"/"midnight_city_m83.json"
    loaded_track = load_track_from_json(saved_path)

    print("다시 읽은 곡: ", loaded_track)