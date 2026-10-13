# AI Music Digging Agent

## 📋 프로젝트 개요

**프로젝트명:** AI Music Digging Agent  
**목표:** 사용자의 자연어 취향과 탐색 의도를 분석해 새로운 음악을 단계적으로 발견할 수 있도록 돕는 AI Agent 구축

현재 Spotify, YouTube Music과 같은 음악 플랫폼은 사용자의 청취 이력과 선호도를 기반으로 개인화 추천을 제공한다.  
하지만 기존 추천은 사용자가 이미 좋아할 가능성이 높은 음악을 제시하는 데 집중되어 있어, 사용자가 원하는 방향으로 새로운 장르나 아티스트를 의도적으로 탐색하는 데에는 한계가 있음.

본 프로젝트는 단순 추천을 넘어, 사용자가 원하는 방향으로 음악을 탐색하고 그 과정까지 확인할 수 있는 **Music Digging Agent**를 구축하는 것을 목표로 함.

### 🎯 핵심 목표

- 자연어 기반 음악 탐색
- 여러 음악 데이터 소스를 활용한 후보 탐색
- PostgreSQL + pgvector 기반 의미 검색
- AI Agent 기반 검색 전략 생성
- 음악 간 연결 관계를 보여주는 Digging Path 제공
- 사용자 피드백 기반 개인화

---

## 🏗️ 시스템 흐름

```text
User
 ↓
Frontend / FastAPI
 ↓
LangGraph Agent
 ↓
Intent 분석
 ↓
검색 전략 생성
 ↓
YouTube Music / Last.fm / MusicBrainz
 ↓
PostgreSQL + pgvector
 ↓
후보 Ranking
 ↓
Digging Path 생성
 ↓
추천 결과
```

---

## 🔄 데이터 파이프라인

```text
Last.fm / MusicBrainz
        ↓
Apache Airflow
        ↓
데이터 수집
        ↓
정제 / 중복 제거
        ↓
Embedding 생성
        ↓
PostgreSQL + pgvector
```

Airflow는 실시간 Agent가 아닌 음악 메타데이터를 수집·정제하고 임베딩을 갱신하는 배치 파이프라인으로 사용.

---

## 🛠️ 기술 스택

| 영역 | 기술 |
|---|---|
| Language | Python |
| Agent | LangGraph |
| LLM | Amazon Bedrock |
| Backend | FastAPI |
| Database | PostgreSQL |
| Vector Search | pgvector |
| Pipeline | Apache Airflow |
| Music Data | YouTube Music, Last.fm, MusicBrainz |
| Cloud | AWS |
| Container | Docker |

---

## 🎵 주요 기능

### 1. 자연어 기반 음악 탐색

사용자가 자연어로 원하는 음악의 방향을 입력한다.

예시:

> “Daft Punk와 비슷하지만 조금 더 마이너한 프렌치 하우스를 찾아줘.”

Agent는 요청에서 탐색 조건을 추출한다.

```json
{
  "seed_artist": "Daft Punk",
  "genre": "French House",
  "popularity": "low"
}
```

---

### 2. 음악 데이터 탐색

- **YouTube Music**: 실제 곡, 아티스트, 앨범 검색
- **Last.fm**: 유사 아티스트, 태그, 장르 정보
- **MusicBrainz**: 아티스트 및 앨범 메타데이터

---

### 3. Vector Search

사용자의 감성적 표현을 Embedding으로 변환하고 PostgreSQL + pgvector에서 의미적으로 유사한 음악을 검색한다.

예시:

> “비 오는 밤에 들을 몽환적인 전자음악”

---

### 4. Digging Path

단순 추천 목록이 아니라 음악 간의 탐색 경로를 제공한다.

```text
Radiohead
 ↓
Thom Yorke
 ↓
Burial
 ↓
Four Tet
 ↓
Floating Points
```

각 단계에는 다음 음악으로 이동한 이유를 함께 제공한다.

---

## 📁 프로젝트 구조

```text
music-digging-agent/

├── app/
│   ├── agents/
│   ├── tools/
│   ├── services/
│   └── api/
│
├── dags/
│   └── music_pipeline.py
│
├── database/
│   ├── schema.sql
│   └── queries/
│
├── frontend/
├── infra/
│   ├── provider.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── s3.tf
│   ├── iam.tf
│   ├── lambda.tf
│   ├── rds.tf
│   ├── network.tf
│   ├── versions.tf
│   └── ...
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 📅 구현 계획

### Phase 1. 기반 구축
- PostgreSQL + pgvector 환경 구성
- Docker 개발 환경 구축
- MusicBrainz / Last.fm API 테스트

### Phase 2. 데이터 구축
- 음악 데이터 수집
- Embedding 생성
- Vector Search 구현

### Phase 3. AI Agent
- LangGraph Agent 구현
- 음악 검색 Tool 연결
- 검색 전략 및 재검색 로직 구현

### Phase 4. 서비스 구현
- FastAPI Backend
- Frontend
- 사용자 피드백 기능

### Phase 5. AWS 연동
- Amazon Bedrock 연결
- Amazon S3 활용
- 필요 시 추가 AWS 서비스 적용

---

## 💰 예상 AWS 비용

초기 개발은 PostgreSQL + pgvector, Apache Airflow, FastAPI를 로컬 Docker 환경에서 운영하고 AWS는 사용량 기반 서비스 위주로 사용하여 고정 비용을 최소화한다.

### 비용 산정 가정

- 월 사용자 요청: 약 1,000회
- 사용자 요청 1회당 Bedrock LLM 호출: 평균 2회
- LLM 1회 호출: 입력 약 2,000 tokens / 출력 약 500 tokens
- 월 총 사용량: 입력 약 4M tokens / 출력 약 1M tokens
- 음악 원본 및 가공 데이터: 수 GB 이하
- PostgreSQL / Airflow: 로컬 Docker 환경 사용

### 월 예상 비용

| 서비스 | 사용 방식 | 예상 월 비용 |
|---|---|---:|
| **Amazon Bedrock** | Intent 분석, 탐색 계획, 추천 설명 생성 | 약 $1 ~ $30 |
| **Amazon S3** | 음악 데이터 및 결과 백업 | $0.1 미만 예상 |
| **AWS Lambda** | 필요 시 API/배치 함수 실행 | 소규모 사용 시 $0에 근접 |
| **API Gateway (선택 사항)** | 서비스 배포 시 HTTP API | 소규모 사용 시 $0 ~ $1 |
| **CloudWatch (선택 사항)** | 기본 로그 및 모니터링 | 소규모 사용 시 $0에 근접 |
| **PostgreSQL + pgvector** | 로컬 Docker | $0 |
| **Apache Airflow** | 로컬 Docker | $0 |
| **예상 합계** | MVP / 개발 단계 | **약 $1 ~ $31 / 월** |

> Bedrock 비용은 선택하는 모델에 따라 가장 크게 달라진다. 저비용 모델을 사용할 경우 월 1달러 수준까지 낮출 수 있지만, 고성능 모델을 모든 Agent 단계에서 사용할 경우 비용이 증가한다.

### 비용 절감 전략

- Agent의 모든 단계를 LLM으로 처리하지 않고 검색, 필터링, Ranking은 Python 로직으로 구현
- LLM 호출을 사용자 요청당 약 2회로 제한
- 개발 단계에서는 RDS 대신 로컬 PostgreSQL + pgvector 사용
- Amazon MWAA 대신 로컬 Docker 기반 Airflow 사용
- OpenSearch 대신 pgvector 사용
- 대량 Embedding은 실시간 생성이 아니라 Airflow 배치 작업으로 처리
- 실제 서비스 배포가 필요한 단계에서만 Lambda, API Gateway, RDS 도입 검토

※ 실제 비용은 선택한 Bedrock 모델, AWS Region, 요청량 및 데이터 크기에 따라 달라질 수 있으므로 최종 배포 단계에서 다시 산정한다.

---

## 🎯 성공 기준

| 항목 | 검증 기준 |
|---|---|
| 자연어 분석 | Seed Artist, Genre, Mood 등 탐색 조건 추출 |
| 음악 검색 | 여러 음악 데이터 소스 검색 성공 |
| Vector Search | 의미 기반 음악 검색 결과 확인 |
| Agent 동작 | 상황에 따라 Tool 선택 및 재검색 |
| Digging Path | 음악 간 연결 경로 생성 |
| 개인화 | 사용자 피드백이 이후 추천에 반영 |

---

## 핵심 차별점

기존 음악 플랫폼은 **“사용자가 좋아할 음악”을 추천하는 데 집중**한다.

본 프로젝트는 **“사용자가 원하는 방향으로 새로운 음악을 찾아가는 과정”을 지원**하는 것을 목표로 한다.

즉, 단순 Recommendation이 아니라 **Discovery 중심의 AI Music Digging Agent**를 구현한다.
