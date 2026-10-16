-- 실제 곡 정보와 태그를 저장할 DB 구조를 정의
-- 백터 컬럼은 임베딩 모델과 차원을 정한 뒤 추가

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS tracks (
    musicbrainz_id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    tags TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    disambiguation TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);