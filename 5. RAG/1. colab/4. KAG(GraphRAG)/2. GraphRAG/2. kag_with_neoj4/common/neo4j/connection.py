from neo4j import GraphDatabase
from langchain_core.documents import Document

from .query_templates import CypherQueryTemplates

class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Neo4jConnection(metaclass=Singleton):
    """Neo4j 데이터베이스 연결 및 작업을 위한 클래스"""
    
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        print("Neo4j 연결 성공!")

    
    def close(self):
        if self.driver is not None:
            self.driver.close()
            print("Neo4j 연결 종료")
    
    def execute_query(self, query:str, parameters:dict=None) -> list:

        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [r.data() for r in result]

    def execute_query_templates(self, template:str, parameters:dict=None) -> list:
        if template not in CypherQueryTemplates.__members__:
            raise Exception("[Neo4jConnection] 올바른 template이 아닙니다.")

        query = CypherQueryTemplates[template].build(**parameters)
        results = self.execute_query(query)

        return [
            Document(
                page_content=f"""
                [뉴스 제목] {result['title']}
                [뉴스 내용] 
                {result['content']}
                """,
                metadata={
                    "publisher_name":result['publisher_name'],
                    "reporter_name":result['reporter_name'],
                    "publish_date":result['publish_date'],
                    "source":result['news_link'],
                }
            ) for result in results
        ]



if __name__ == "__main__":
    Neo4jConnection(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="test1234"
    )

