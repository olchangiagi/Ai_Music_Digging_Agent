'''
- 음악 탐색에서 사용하는 곡 한 개의 공통 데이터 형태를 정의
- 데이터 읽기, 검색, Agent가 같은 필드 이름을 사용하게 함
'''

# 곡 데이터 클래스의 생성자와 출력 형태를 자동으로 만들어줌
from dataclasses import dataclass

# 아래 선언한 필드를 바탕으로 생성자, 출력 형태, 값 비교 기능 생성
@dataclass
class Track:
    title: str      # 곡 제목
    artist: str     # 아티스트 이름
    tags: list[str] # 장르, 분위기를 나타내는 키워드들