from enum import Enum

class CypherQueryTemplates(Enum):
    """다양한 질문 유형을 Enum으로 관리하는 Cypher 템플릿"""

    NEWS_BY_CATEGORY = "news_by_category"
    NEWS_BY_PUBLISHER = "news_by_publisher"
    NEWS_BY_REPORTER = "news_by_reporter"

    def build(self, **kwargs):
        """템플릿 유형에 따라 Cypher 쿼리 생성"""
        if self is CypherQueryTemplates.NEWS_BY_CATEGORY:
            category_name = kwargs["category_name"]
            limit_no = kwargs["limit_no"]
            return f"""
            MATCH (n:News)-[:BELONGS_TO]->(c:Category {{name: "{category_name}"}})
            MATCH (n)-[:PUBLISHED_BY]->(p:Publisher)
            MATCH (n)-[:WRITTEN_BY]->(r:Reporter)
            RETURN n.title, n.content, 
                   p.name as publisher_name, 
                   r.name as reporter_name, 
                   n.publishDate as publish_date,
                   n.link as news_link
            LIMIT {limit_no}
            """

        if self is CypherQueryTemplates.NEWS_BY_PUBLISHER:
            publisher_name = kwargs["publisher_name"]
            limit_no = kwargs["limit_no"]
            return f"""
            MATCH (n:News)-[:PUBLISHED_BY]->(p:Publisher {{name: "{publisher_name}"}})
            MATCH (n)-[:BELONGS_TO]->(c:Category)
            MATCH (n)-[:WRITTEN_BY]->(r:Reporter)
            RETURN n.title, n.content, 
                   p.name as publisher_name, 
                   r.name as reporter_name, 
                   n.publishDate as publish_date,
                   n.link as news_link
            LIMIT {limit_no}
            """

        if self is CypherQueryTemplates.NEWS_BY_REPORTER:
            reporter_name = kwargs["reporter_name"]
            limit_no = kwargs["limit_no"]
            return f"""
            MATCH (n:News)-[:WRITTEN_BY]->(r:Reporter {{name: "{reporter_name}"}})
            MATCH (n)-[:BELONGS_TO]->(c:Category)
            MATCH (n)-[:PUBLISHED_BY]->(p:Publisher)
            RETURN n.title, n.content, 
                   p.name as publisher_name, 
                   r.name as reporter_name, 
                   n.publishDate as publish_date,
                   n.link as news_link
            LIMIT {limit_no}
            """

        raise ValueError(f"지원하지 않는 템플릿: {self}")


if __name__ == "__main__":
    # 카테고리로 뉴스 검색
    query = CypherQueryTemplates.NEWS_BY_CATEGORY.build(
        category_name="경제", limit_no=3)
    print(query)