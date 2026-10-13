'''
- 음악 탐색에 사용할 곡 데이터 기본 형태 작성
'''
from dataclasses import dataclass

@dataclass
class Track: 
    title: str
    artist: str
    tags: list[str]