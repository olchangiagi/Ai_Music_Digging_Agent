'''
- bedrock 연결 테스트
'''

import os
import boto3
from dotenv import load_dotenv

load_dotenv()

bedrock = boto3.client(
    "bedrock-runtime",
    region_name=os.environ["AWS_REGION"],
)
# print("Bedrock client region:", bedrock.meta.region_name)
# print("AWS_REGION: ", os.getenv("AWS_REGION"))
# print("BEDROCK_CHAT_MODEL: ", os.getenv("BEDROCK_CHAT_MODEL"))
# print("BEDROCK_EMBED_MODEL: ", os.getenv("BEDROCK_EMBED_MODEL"))

# bedrock api chat model 응답 확인
def ask_bedrock(prompt:str) -> str:
    response = bedrock.converse(
        modelId = os.environ["BEDROCK_CHAT_MODEL"],
        messages = [
            {"role": "user", "content": [{"text": prompt}]}
        ],
        inferenceConfig = {"maxTokens": 64}
    )
    return response["output"]["message"]["content"][0]["text"]

if __name__ == "__main__":
    print(ask_bedrock("한 문장으로 인사해 주세요."))