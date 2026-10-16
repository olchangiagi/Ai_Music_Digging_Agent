'''
- MusicBrainz 후보 선택 로직을 API 호출 없이 검증
'''

import unittest
from app.music_data import select_recording_by_id

class TestSelectRecordingById(unittest.TestCase):
    # 원하는 ID가 첫 번째가 아니여도 정확히 선택하는지 확인
    def test_selectes_matching_id(self):
        candidates = [{"id": "first"}, {"id": "wanted"}]

        selected = select_recording_by_id(candidates, "wanted")

        self.assertEqual(selected["id"], "wanted")

    # 요청한 ID가 없다면 다른 후보를 대신 선택하지 않는지 확인
    def test_raises_for_missing_id(self):
        candidates = [{"id": "first"}, {"id": "second"}]

        with self.assertRaises(ValueError):
            select_recording_by_id(candidates, "missing")