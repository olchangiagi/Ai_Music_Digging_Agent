'''
- 현재 단계에서 Bedrock 채팅 모델 연결을 확인하는 싫행 파일
- 이후 음악 탐색 기능을 실행하는 진입점으로 확장 
'''

# 1. 모듈 불러오기
import os # 환경변수에서 AWS 리전과 모델 이름을 불러오기 위해 사용
import boto3 # Python에서 AWS Bedrock 서비스를 호출하기 위해 사용
from dotenv import load_dotenv # .env파일의 설정값을 환경변수로 읽기 위해 사용
from app.catalog import load_tracks # JSON 파일을 Track 목록으로 읽기
from app.search import search_by_tag # Track 목록에서 태그로 곡 찾기


# 프로젝트 root의 .env 값을 현재 python 프로그램의 환경변수로 읽어옴
load_dotenv()

# Bedrock 모델에 요청을 보낼 클라이언트 객체 준비
bedrock = boto3.client(
    "bedrock-runtime",                       # 모델 추론 요청을 처리하는 AWS 서비스
    region_name = os.environ["AWS_REGION"]   # .env에서 읽은 리전을 명시적으로 사용
)

def ask_bedrock(prompt: str) -> str:
    """
        입력 문장을 Bedrock 채팅 모델에 보내고 답변 텍스트를 반환
    """
    # Bedrock에 요청을 보내고 응답 전체를 response에 저장함
    response = bedrock.converse(
        modelId = os.environ["BEDROCK_CHAT_MODEL"], # .env에서 Chat_model 가져오기
        
        # 모델에 전달할 대화 메시지 목록
        messages = [
            {
                "role" : "user",                # 이 메시지를 보내는 주체
                "content" : [{"text" : prompt}] # 함수에 받은 질문 문장
            }
        ],

        # 모델이 생성할 답변의 최대 길이 
        inferenceConfig = {"maxTokens" : 64},
    )
    # 응답의 첫 번째 내용 블록에서 생성된 문장만 꺼내 호출한 곳으로 반환
    return response["output"]["message"]["content"][0]["text"]

# 이 파일을 직접 수행할 때만 아래 테스트 수행
if __name__ == "__main__":
    # 샘플 곡을 읽고, dreamy 태그가 있는 곡을 검색
    tracks = load_tracks()
    matches = search_by_tag(tracks, "dreamy")
    
    # 함수가 돌려준 답변 문자열을 터미널에 출력
    # 검색된 곡의 제목과 아티스트를 한 곡씩 출력
    for track in matches:
        print(f"{track.title} - {track.artist}") 
    # print(ask_bedrock('한 문장으로 인사해 주세요.'))

    # 존재하지 않는 태그로 검색하면 빈 목록이 반환되는지 확인
    no_matches = search_by_tag(tracks, "없는 태그")
    print("검색 결과 없음", no_matches)