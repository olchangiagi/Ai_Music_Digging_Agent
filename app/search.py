'''
- 전달받은 Track 목록에서 요청한 태그와 일치하는 곡을 찾음
'''
# Track을 가져오기
from app.models import Track

# 곡 목록에서 지정한 태그가 있는 곡만 골라 새 목록으로 돌려줌
def search_by_tag(tracks: list[Track], tag: str) -> list[Track]:
    # 입력한 태그를 대소문자 구분 없이 비교할 형태로 변환
    normalized_tag = tag.casefold()
    # 검색 결과를 담을 빈 목록 생성
    matches: list[Track] = []

    # 전달 받은 곡을 하나씩 살펴봄
    for track in tracks:
        # 곡의 태그 목록에 요청한 태그가 있다면 결과에 추가
        # 곡에 저장된 태그도 같은 방식으로 바꿔 비교
        normalized_tags = [item.casefold() for item in track.tags]
        if normalized_tag in normalized_tags:
            matches.append(track)

    # 조건에 맞았던 곡들만 돌려줌
    return matches