'''
- 곡 수집 함수가 선택한 ID의 Track을 DB 저장 함수에 전달하는지 확인
'''

import unittest
from unittest.mock import patch
from app.ingest import ingest_track_by_id
from app.models import Track

class TestIngestTrackById(unittest.TestCase):
    def test_saves_track_built_from_selected_id(self):
        recording_id = "e83bc6ba-eff9-412c-8c11-5153672f25e7"
        track = Track(
            title="Midnight City",
            artist="M83",
            tags=["shoegaze"],
            musicbrainz_id=recording_id,
        )

        # 외부 조회와 DB 저장을 가짜 함수로 바꿔 연결 방식만 확인
        with patch(
            "app.ingest.build_track_from_musicbrainz_id",
            return_value=track,
        ) as mock_build:
            with patch("app.ingest.save_track") as mock_save:
                result = ingest_track_by_id(recording_id)

        mock_build.assert_called_once_with(recording_id)
        mock_save.assert_called_once_with(track)
        self.assertIs(result, track)