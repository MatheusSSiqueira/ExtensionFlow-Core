import os
from typing import Any, Dict, List

import psycopg
from google import genai
from google.genai import types


EMBEDDING_DIMENSION = 768
EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")


def _database_url() -> str:
    database_url = os.environ["DATABASE_URL"]
    return database_url.replace("postgresql+asyncpg://", "postgresql://", 1)


def _embedding_client() -> genai.Client:
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def _embed(text: str) -> List[float]:
    response = _embedding_client().models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=EMBEDDING_DIMENSION),
    )
    return list(response.embeddings[0].values)


def _as_pgvector(values: List[float]) -> str:
    return "[{}]".format(",".join(str(value) for value in values))


class PgVectorStore:
    def add_documents(self, chunks: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """Insere blocos e seus embeddings no PostgreSQL com pgvector."""
        if not chunks:
            return

        rows = []
        for index, chunk in enumerate(chunks):
            metadata = metadatas[index] if index < len(metadatas) else {}
            document_id = metadata.get("document_id", metadata.get("source", ids[index]))
            tenant_id = metadata.get("tenant_id")
            rows.append(
                (
                    ids[index],
                    tenant_id,
                    str(document_id),
                    chunk,
                    _as_pgvector(_embed(chunk)),
                )
            )

        with psycopg.connect(_database_url()) as connection:
            with connection.cursor() as cursor:
                cursor.executemany(
                    """
                    INSERT INTO document_embeddings
                        (id, tenant_id, document_id, chunk_text, embedding)
                    VALUES (%s, %s, %s, %s, %s::vector)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    rows,
                )

        print(f"[{len(rows)}] blocos indexados no pgvector.")

    def search(self, query: str, n_results: int = 4) -> List[Dict[str, Any]]:
        """Busca os blocos mais relevantes usando distância cosseno."""
        query_embedding = _as_pgvector(_embed(query))

        with psycopg.connect(_database_url()) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT document_id, chunk_text
                    FROM document_embeddings
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                    """,
                    (query_embedding, n_results),
                )
                results = cursor.fetchall()

        return [
            {
                "content": chunk_text,
                "metadata": {"source": document_id},
            }
            for document_id, chunk_text in results
        ]


# Compatibilidade para código que importava a classe pelo nome antigo.
ChromaVectorStore = PgVectorStore
vector_db = PgVectorStore()