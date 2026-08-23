"""Camada de persistência e busca vetorial usando ChromaDB + Gemini Embeddings.

Este módulo encapsula a criação de embeddings via Gemini e oferece uma
classe simples para armazenar e buscar trechos de regulamentos.
"""

import os
import chromadb
import google.generativeai as genai
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from app.core.config import settings

# Inicializa a chave para geração de embeddings (Gemini)
genai.configure(api_key=settings.gemini_api_key)


class GeminiEmbeddingFunction(EmbeddingFunction):
    """Adaptador que converte textos em embeddings usando o Gemini.

    Implementa a interface exigida pelo ChromaDB para funções de embedding.
    """

    def __call__(self, input: Documents) -> Embeddings:
        result = genai.embed_content(
            model="models/gemini-embedding-2",
            content=input,
            task_type="retrieval_document"
        )
        return result['embedding']


class DocumentStore:
    def __init__(self, persist_directory: str = "data/chroma_db"):
        """Inicializa o cliente ChromaDB e prepara a collection usada pela aplicação.

        Args:
            persist_directory: Pasta onde o banco persistente será armazenado.
        """
        os.makedirs(persist_directory, exist_ok=True)

        # Cliente persistente para garantir que embeddings e metadados fiquem no disco
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_function = GeminiEmbeddingFunction()

        # Cria ou carrega a coleção onde serão guardados os regulamentos
        self.collection = self.client.get_or_create_collection(
            name="unicesumar_regulations",
            embedding_function=self.embedding_function
        )

    def add_chunks(self, chunks: list[str], metadatas: list[dict], ids: list[str]):
        """Insere ou atualiza documentos (pedaços de regulamento) na coleção."""
        self.collection.upsert(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query_text: str, n_results: int = 3) -> str:
        """Busca os trechos mais relevantes para uma consulta.

        Retorna uma string com os trechos encontrados separados por duas quebras
        de linha, adequada para ser enviada ao LLM como contexto.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

        if results and results['documents']:
            found_chunks = results['documents'][0]
            return "\n\n".join(found_chunks)
        return "Nenhuma informação relevante encontrada no regulamento."


vector_db = DocumentStore()