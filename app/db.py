'''
- PostgreSQL 접속 정보를 .env에서 읽고 연결 생성
- 곡 저장, 조회 코드가 같은 연결 방법을 사용하게 함
'''

import os 
import psycopg
from pathlib import Path
from dotenv import load_dotenv
from uuid import UUID
from app.models import Track

# 어느 폴더에서나 실행하는 프로젝트 루트의 .env를 읽음
load_dotenv(Path(__file__).resolve().parent.parent/".env")

# .env의 DB 설정으로 PostgreSQL 연결을 만들어 반환
def get_connection() -> psycopg.Connection:
    # 필수 설정이 빠졌다면 조용히 다른 DB에 연결하지 않고 오류를 냄
    return psycopg.connect(
        host = os.environ["DB_HOST"],
        port = int(os.environ["DB_PORT"]),
        dbname = os.environ["DB_NAME"],
        user = os.environ["DB_USER"],
        password = os.environ["DB_PASSWORD"]
    )

# MusicBrainz ID가 있는 Track 한 건을 tracks 테이블에 저장
# 같은 ID가 이미 있으면 제목, 아티스트, 태그, 설명을 갱신
def save_track(track: Track) -> None:
    # DB에서 MusicBrainz ID가 기본 키이므로, ID가 없는 샘플 곡은 저장하지 않음
    if not track.musicbrainz_id:
        raise ValueError("저장하려는 곡에 MusicBrainz ID가 없음")

    # UUID 형태가 잘못됐다면 DB에 보내기 전에 오류가 남
    recording_id = UUID(track.musicbrainz_id)

    # 정상 종료했다면 저장을 확정하고, 오류가 나면 취소한 뒤 연결을 닫음
    with get_connection() as conn:
        conn.execute(
            """
                INSERT INTO tracks (musicbrainz_id, title, artist, tags, disambiguation)
                Values (%s, %s, %s, %s, %s)
                ON CONFLICT (musicbrainz_id) DO UPDATE SET
                    title = EXCLUDED.title,
                    artist = EXCLUDED.artist,
                    tags = EXCLUDED.tags,
                    disambiguation = EXCLUDED.disambiguation
            """,
            (
                recording_id,
                track.title,
                track.artist,
                track.tags,
                track.disambiguation
            ),
        )

# MusicBrainz ID로 저장한 곡을 찾아 Track으로 반환
# ID 형식은 올바르지만 저장된 곡이 없으면 None 반환
def get_track_by_id(recording_id: str) -> Track | None:
    # 잘못된 ID 형식은 조회 전에 오류로 알림
    valid_id = UUID(recording_id)

    with get_connection() as conn:
        # 입력값은 SQL 문자열에 직접 붙이지 않고 매개변수로 전달
        row = conn.execute(
            """
                SELECT title, artist, tags, musicbrainz_id, disambiguation
                FROM tracks
                WHERE musicbrainz_id = %s
            """,
            (valid_id,),
        ).fetchone()

    # 형식을 올바르지만 DB에 없는 ID라면 곡이 없음을 나타냄
    if row is None:
        return None

    # DB의 한 행을 프로젝트에서 사용하는 track 형태로 되돌림
    return Track(
        title = row[0],
        artist = row[1],
        tags = row[2],
        musicbrainz_id = str(row[3]),
        disambiguation = row[4]
    )

# DB에 저장된 곡 중 지정한 태그를 가진 곡을 모두 반환
def search_tracks_by_tag(tag: str) -> list[Track]:
    with get_connection() as conn:
        rows = conn.execute(
            """
                SELECT title, artist, tags, musicbrainz_id, disambiguation
                FROM tracks
                WHERE EXISTS (
                    SELECT 1
                    FROM unnest(tracks.tags) AS stored_tag(tag_value)
                    WHERE LOWER(tag_value) = LOWER(%s)
                )
                ORDER BY artist, title, musicbrainz_id
            """,
            (tag, ),
        ).fetchall()

    # 조회된 DB 행들을 Track 객체 목록으로 변환
    return [
        Track(
            title = row[0],
            artist = row[1],
            tags = row[2],
            musicbrainz_id = str(row[3]),
            disambiguation = row[4]
        )
        for row in rows
    ]