from elasticsearch import Elasticsearch
import warnings

# SSL 경고 무시 (개발 환경용)
warnings.filterwarnings('ignore')

def create_client(hosts:list=["http://localhost:9200"], id:str="elastic", pw:str="changeme123!"):
    es_client = Elasticsearch(
        hosts=hosts,  # 리스트 형태로, scheme 포함
        basic_auth=(id, pw),  # 인증 정보 (보안 활성화 시 필수)
        verify_certs=False,
        ssl_show_warn=False,
        request_timeout=30,
        max_retries=3,
        retry_on_timeout=True,
        # 호환성 헤더 비활성화 (개발 환경용)
        headers={"accept": "application/json", "content-type": "application/json"}
    )
    
    # 연결 확인
    if es_client.ping():
        print("Elasticsearch 연결 성공!")
        print()
        
        # 클러스터 정보
        info = es_client.info()
        print(f"버전: {info['version']['number']}")
        print(f"클러스터 이름: {info['cluster_name']}")
        print(f"노드 이름: {info['name']}")
        return es_client
    else:
        print("Elasticsearch 연결 실패 (ping 실패)")


if __name__ == "__main__":
    create_client()