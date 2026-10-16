'''
- MusicBrainz의 곡 정보와 Last.fm의 태그를 하나의 Track으로 연결
- 검색 결과 중 사용할 recording을 선택하는 과정을 담당
'''

from app.models import Track
from app.lastfm import fetch_track_top_tags, extract_tag_names
from app.musicbrainz import search_recordings, recording_to_track, get_recording_by_id
from dataclasses import asdict # Track 객체를 딕셔너리로 변환
import json # Python 데이터를 Json 문자열로 변환

# 제목과 artist로 MusicBrainz recording 후보들을 검색
def find_recording_candidates(title: str, artist: str) -> list[dict]:
    # 두 조건을 함께 사용해 동명 곡을 줄임
    query = f'recording:"{title}" AND artist:"{artist}"'

    # 검색 응답에서 recording 목록만 꺼냄
    result = search_recordings(query)
    return result.get("recordings", [])

# 후보 목록에서 지정한 MusicBrainz ID와 일치하는 recording을 찾음
def select_recording_by_id(candidates: list[dict], recording_id: str) -> dict:
    for candidate in candidates:
        if candidate.get("id") == recording_id:
            return candidate

    # 현재 검색 결과에 해당 ID가 없으면 다른 곡을 대신 선택하지 않음
    raise ValueError(f"검색 후보에서 ID를 찾지 못함: {recording_id}")

# 이미 선택한 MusicBrainz recording에 Last.fm 태그를붙여 Track 생성
def build_track_from_recording(recording: dict) -> Track:
    # MusicBrainz 데이터를 Track 형태로 만듬
    track = recording_to_track(recording)

    # 곡의 아티스트와 제목으로 태그를 가져와 채움
    tag_data = fetch_track_top_tags(track.artist, track.title)
    track.tags = extract_tag_names(tag_data)

    return track

# MusicBrainz ID로 조회한 후, 공통 함수에서 태그까지 연결
def build_track_from_musicbrainz_id(recording_id: str) -> Track:
    # ID로 recording을 조회하고 Track 형태로 변환
    recording = get_recording_by_id(recording_id)

    return build_track_from_recording(recording)

# 이 파일을 직접 실행할 때만 선택한 recording을 확인
if __name__ == "__main__":
    candidates = find_recording_candidates("Midnight City", "M83")
    print("후보 수: ", len(candidates))

    # 각 후보의 식별에 필요한 정보를 출력
    for recording in candidates:
        track = recording_to_track(recording)

        # 후보가 연결된 발매 제목을 최대 3개 확인
        release_titles = [
            release.get("title", "제목 없음")
            for release in recording.get("releases", [])[ :3]
        ]

        print(
            f"{track.title} - {track.artist} | "
            f"길이(ms): {recording.get('length')} | "
            f"설명: {track.disambiguation or '없음'} | "
            f"발매: {release_titles} | "
            f"ID: {track.musicbrainz_id}"
        )

    # 후보 위치가 아닌 MusicBrainz ID로 선택
    selected_id = "e83bc6ba-eff9-412c-8c11-5153672f25e7"
    selected_recording= select_recording_by_id(candidates, selected_id)
    # 선택한 recording을 Track으로 바꾸고 Last.fm 태그를 채움
    selected_track = build_track_from_recording(selected_recording)

    print("선택한 곡: ", selected_track.title, "-", selected_track.artist)
    print("선택한 ID: ", selected_track.musicbrainz_id)
    print("선택한 곡의 태그: ", selected_track.tags[ :10])

    # Track에 정의된 필드를 저장하기 쉬운 딕셔너리로 바꿈
    track_data = asdict(selected_track)
    json_text = json.dumps(track_data, ensure_ascii = False, indent = 2)
    print("저장할 JSON:\n ", json_text)

    # # 새 파일에만 JSON을 씀. 같은 이름의 파일이 있으면 덮어쓰지 않음
    # with open('data/midnight_city_m83.json', "x", encoding = "utf-8") as output_file:
    #     output_file.write(json_text)


