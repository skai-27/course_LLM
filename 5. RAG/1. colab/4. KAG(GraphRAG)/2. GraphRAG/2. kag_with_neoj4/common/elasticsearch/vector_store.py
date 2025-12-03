from langchain_core.vectorstores.base import VectorStore
from langchain_core.documents import Document
from typing import List, Tuple

from connection import create_client


class Singleton(type(VectorStore)):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ElasticsearchVectorStore(VectorStore, metaclass=Singleton):
    """Elasticsearch 기반 VectorStore"""

    def __init__(self, index_name, embeddings, 
                 hosts:list=["http://localhost:9200"], id:str="elastic", pw:str="changeme123!"):
        self.es_client = create_client(hosts=hosts, id=id, pw=pw)
        self.index_name = index_name
        self._embeddings = embeddings

    @classmethod
    def from_texts(cls, **kwargs):
        """VectorStore 상속을 받기 위한 필수 함수 선언"""
        pass

    def __search_hybrid(self, query: str, k: int):
        # 쿼리 임베딩
        query_embedding = self._embeddings.embed_query(query)
        
        # 하이브리드 검색 쿼리
        search_query = {
            "query": {
                "bool": {
                    "should": [
                        # BM25 키워드 검색
                        {
                            "match": {
                                "text": {
                                    "query": query,
                                    "boost": 1.0  # 키워드 가중치
                                }
                            }
                        }
                    ]
                }
            },
            "knn": {
                "field": "embedding",
                "query_vector": query_embedding,
                "k": k,
                "num_candidates": 100,
                "boost": 2.0  # 벡터 검색 가중치
            },
            "size": k,
            "_source": ["text", "metadata"]
        }
    
        # 검색 실행
        return self.es_client.search(index=self.index_name, body=search_query)

    def __minmaxscaling_score(self, hits:list)-> tuple:
        raw_scores = [hit['_score'] for hit in hits]
        min_score = min(raw_scores)
        max_score = max(raw_scores)
        score_range = max_score - min_score if max_score != min_score else 1.0  # 0 나눔 방지
        return score_range, min_score

    def __convert_hits_to_documents(self, hits:list, score_range:float, min_score:float) -> list:
        documents = []
        for hit in hits:
            doc = Document(
                page_content=hit['_source']['text'],
                metadata=hit['_source'].get('metadata', {})
            )
            norm_score = (hit['_score'] - min_score) / score_range
            documents.append((doc, norm_score))

        return documents

    def hybrid_search_with_score(
        self, query: str, k: int = 4
    ) -> List[Tuple[Document, float]]:
        """
        하이브리드 검색: BM25 + Embedding 유사도
        - _score를 Min-Max 정규화 후 반환
        """
        # 1. 검색 실행
        hits = self.__search_hybrid(query, k)['hits']['hits']

        if not hits:
            return []

        # 2. _score 추출
        score_range, min_score = self.__minmaxscaling_score(hits)

        # 3. 정규화 후 Document와 튜플로 반환
        return self.__convert_hits_to_documents(hits, score_range, min_score)
