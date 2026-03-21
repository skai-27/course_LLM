import os
from pathlib import Path
from typing import List

from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

from common.elasticsearch_vector import ElasticsearchVectorStore

load_dotenv()


def split_paragraphs(text: str) -> List[str]:
    return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]


def ensure_index(es: Elasticsearch, index_name: str, dims: int) -> None:
    if es.indices.exists(index=index_name):
        return

    es.indices.create(
        index=index_name,
        body={
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
        },
    )


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
    ensure_index(es=es, index_name=index_name, dims=dims)

    bulk_ops = []
    for source in ["rag-keywords.txt", "web-keywords.txt"]:
        content = (data_dir / source).read_text(encoding="utf-8")
        for chunk_id, chunk in enumerate(split_paragraphs(content)):
            bulk_ops.append({"index": {"_index": index_name}})
            bulk_ops.append(
                {
                    "text": chunk,
                    "embedding": embeddings.embed_query(chunk),
                    "metadata": {"source": source, "chunk_id": chunk_id},
                }
            )

    if bulk_ops:
        es.bulk(operations=bulk_ops, refresh=True)
    print(f"Indexed chunks: {len(bulk_ops) // 2} -> index={index_name}")

    store = ElasticsearchVectorStore(
        es_client=es,
        index_name=index_name,
        embeddings=embeddings,
        k=3,
    )
    preview = store.similarity_search("Semantic Search가 뭐야?", k=2)
    print("Sample retrieval docs:", len(preview))


if __name__ == "__main__":
    main()
