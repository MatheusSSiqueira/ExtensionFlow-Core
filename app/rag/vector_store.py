import os
import chromadb
import google.generativeai as genai
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from app.core.config import settings

# Configura a chave para habilitar a criação dos embeddings
genai.configure(api_key=settings.gemini_api_key)

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        result = genai.embed_content(
            model="models/gemini-embedding-2",
            content=input,
            task_type="retrieval_document"
        )
        return result['embedding']

class DocumentStore:
    def __init__(self, persist_directory: str = "data/chroma_db"):
        """Inicializa o banco de dados e cria a pasta se não existir."""
        os.makedirs(persist_directory, exist_ok=True)
        
        # O PersistentClient garante que os dados sejam salvos no HD e não se percam
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_function = GeminiEmbeddingFunction()
        
        # Cria ou carrega a "tabela" (collection) onde ficarão os regulamentos
        self.collection = self.client.get_or_create_collection(
            name="unicesumar_regulations",
            embedding_function=self.embedding_function
        )
    
    def add_chunks(self, chunks: list[str], metadatas: list[dict], ids: list[str]):
        """Salva os pedaços de texto no banco de dados."""
        self.collection.upsert(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        
    def search(self, query_text: str, n_results: int = 3) -> str:
        """Busca os trechos mais relevantes do regulamento para responder à dúvida."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        if results and results['documents']:
            found_chunks = results['documents'][0]
            return "\n\n".join(found_chunks)
        return "Nenhuma informação relevante encontrada no regulamento."

vector_db = DocumentStore()