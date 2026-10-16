'''
- 선택한 MusicBrainz ID의 곡 정보를 수집하고 DB에 저장
- 데이터 수집 과정과 DB 저장 과정을 연결
'''

from app.db import save_track
from app.models import Track
from app.music_data import build_track_from_musicbrainz_id

# 저장한 recording ID의 곡을 보강해 저장하고, 저장한 Track을 반환
def ingest_track_by_id(recording_id: str) -> Track:
    # MusicBrainz에서 조회하고 Last.fm 태그를 붙임
    track = build_track_from_musicbrainz_id(recording_id)

    # 완성된 Track을 PostgreSQL에 저장
    save_track(track)

    return track