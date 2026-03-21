# LangGraph 기반 RAG + MCP 호출 실습

이 폴더는 `Elasticsearch VectorDB`와 `LangGraph`, `MCP`를 함께 사용해
실무형 RAG 에이전트를 만드는 강의/실습 자료입니다.

## 학습 목표

- `data` 폴더의 텍스트를 임베딩해 Elasticsearch에 인덱싱한다.
- `common/elasticsearch_vector.py`를 활용해 벡터/하이브리드 검색을 수행한다.
- LangGraph로 질문 라우팅(로컬 RAG vs MCP 도구 호출) 그래프를 구성한다.
- MCP 도구(SQL 조회, 외부 API 조회)를 LLM 도구 호출로 연결한다.

## 현재 폴더 구조

```text
3. MCP with LangChain/
├─ README.md
├─ build_rag_index.py
├─ mcp_with_langgraph_rag.py
├─ common/
│  ├─ elasticsearch_vector.py
│  └─ ...
├─ data/
│  ├─ rag-keywords.txt
│  └─ web-keywords.txt
└─ elasticsearch/
   ├─ docker-compose.yml
   └─ README.md
```

## 1) 실습 환경 준비

### 1-1. Elasticsearch 실행

```bash
cd elasticsearch
docker-compose up -d
```

상세 옵션은 `elasticsearch/README.md`를 참고하세요.

### 1-2. Python 패키지 설치

```bash
pip install langgraph langchain langchain-openai \
            langchain-mcp-adapters elasticsearch python-dotenv
```

필요 시 추가:

```bash
pip install langchain-core typing-extensions
```

### 1-3. 환경 변수 설정(.env 예시)

```env
# LLM
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

# Embedding (OpenAI)
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Elasticsearch
ES_URL=http://localhost:9200
ES_USER=elastic
ES_PASSWORD=changeme123!
ES_INDEX=course_keywords

# MCP (옵션)
# 미설정 시 기본값:
# - MCP_SERVER_PYTHON=python
# - MCP_SERVER_SCRIPT=../2. MCP with SQL/example_sql_mcp.py
MCP_SERVER_PYTHON=python
MCP_SERVER_SCRIPT=
```

`mcp_with_langgraph_rag.py` 실행 시 프로젝트 루트 아래 `mcp_workspace/`를 자동 생성하고,
MCP 파일 도구(`fs_read_text_file`, `fs_write_text_file`)의 허용 루트로 사용합니다.

## 2) RAG 인덱스 생성 예제

아래 스크립트는 `data/rag-keywords.txt`, `data/web-keywords.txt`를 읽어
문단 단위로 쪼갠 뒤 Elasticsearch 인덱스에 저장합니다.

파일: `build_rag_index.py`

```python
import os
from pathlib import Path
from typing import List

from elasticsearch import Elasticsearch
from langchain_openai import OpenAIEmbeddings

from common.elasticsearch_vector import ElasticsearchVectorStore


def split_paragraphs(text: str) -> List[str]:
    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
    return chunks


def ensure_index(es: Elasticsearch, index_name: str, dims: int = 1024) -> None:
    if es.indices.exists(index=index_name):
        return

    mapping = {
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": dims,
                    "index": True,
                    "similarity": "cosine",
                },
                "metadata": {"type": "object"},
            }
        }
    }
    es.indices.create(index=index_name, body=mapping)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"

    es = Elasticsearch(
        [os.getenv("ES_URL", "http://localhost:9200")],
        basic_auth=(
            os.getenv("ES_USER", "elastic"),
            os.getenv("ES_PASSWORD", "changeme123!"),
        ),
        verify_certs=False,
    )

    index_name = os.getenv("ES_INDEX", "course_keywords")
    embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    embeddings = OpenAIEmbeddings(model=embedding_model)

    dims = len(embeddings.embed_query("dimension probe"))
    ensure_index(es, index_name=index_name, dims=dims)

    files = ["rag-keywords.txt", "web-keywords.txt"]
    bulk_body = []

    for fname in files:
        text = (data_dir / fname).read_text(encoding="utf-8")
        for i, chunk in enumerate(split_paragraphs(text)):
            vec = embeddings.embed_query(chunk)
            bulk_body.append({"index": {"_index": index_name}})
            bulk_body.append(
                {
                    "text": chunk,
                    "embedding": vec,
                    "metadata": {"source": fname, "chunk_id": i},
                }
            )

    if bulk_body:
        es.bulk(operations=bulk_body, refresh=True)
    print(f"Indexed chunks: {len(bulk_body) // 2} -> index={index_name}")

    store = ElasticsearchVectorStore(
        es_client=es,
        index_name=index_name,
        embeddings=embeddings,
        k=3,
    )
    docs = store.similarity_search("Semantic Search가 뭐야?", k=2)
    print("Sample retrieval:", len(docs))


if __name__ == "__main__":
    main()
```

실행:

```bash
python build_rag_index.py
```

## 3) LangGraph 워크플로우 코드 위치 변경

LangGraph 그래프 코드는 실행 스크립트와 분리해 `common`으로 이동했습니다.

- `RAG 경로`: 로컬 Elasticsearch 지식 베이스 검색
- `MCP 경로`: MCP 서버 도구(SQL/API) 호출 후 답변

파일: `mcp_with_langgraph_rag.py`

```python
from common.langgraph_rag_workflow import run_graph
import asyncio

if __name__ == "__main__":
    asyncio.run(run_graph("Semantic Search와 Embedding 차이를 설명해줘"))
    asyncio.run(run_graph("고객별 주문 수를 SQL로 조회해줘"))
```

실행:

```bash
python mcp_with_langgraph_rag.py
```

## 4) 강의 진행안 (90분 예시)

### Part A. 아키텍처 이해 (15분)

- 왜 RAG와 MCP를 같이 써야 하는가
- 로컬 지식(벡터DB) vs 외부 실시간 데이터(API/DB) 분리 전략
- LangGraph를 사용하는 이유(상태/분기/추적)

### Part B. 실습 1 - 인덱싱 (20분)

- `data/*.txt` 구조 확인
- 청크 분리, 임베딩, ES 인덱스 생성
- 샘플 유사도 검색 검증

### Part C. 실습 2 - LangGraph RAG (20분)

- State 설계 (`question`, `route`, `context`, `answer`)
- `route -> retrieve -> answer` 그래프 연결
- 하이브리드 검색 결과 품질 점검

### Part D. 실습 3 - MCP 도구 호출 (20분)

- MCP 서버 도구 목록 확인
- 질문 기반 도구 선택 프롬프트 설계
- DB 질의 / 외부 API 조회 결과 요약

### Part E. 마무리 (15분)

- 실패 케이스 분석(잘못된 라우팅, 검색 누락)
- 개선 과제
  - 라우터를 규칙 기반에서 LLM 기반 분류기로 교체
  - 검색 재순위(Re-rank) 도입
  - MCP 도구 호출 결과를 다시 RAG 컨텍스트에 합성

## 5) 실습 체크리스트

- [ ] Elasticsearch 정상 실행 (`9200`, `5601`)
- [ ] `build_rag_index.py` 인덱싱 성공
- [ ] `mcp_with_langgraph_rag.py`에서 RAG/MCP 분기 동작 확인
- [ ] 질문 유형별 응답 품질 비교 (개념형 vs 실시간 조회형)

## 6) 트러블슈팅 핵심

- ES 인증 오류(401): `ES_USER`, `ES_PASSWORD` 확인
- 임베딩 모델 오류: `OPENAI_API_KEY`, `OPENAI_EMBEDDING_MODEL` 설정 확인
- MCP 호출 실패: MCP 서버 실행 방식(`stdio`/`sse`)과 연결 파라미터 확인
- 라우팅 실패: `mcp_keywords` 보강 또는 LLM 라우터로 교체