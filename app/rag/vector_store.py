import os
import chromadb
from typing import List, Dict, Any

# Estratégia de Persistência "Baked-in" para o Cloud Run
DB_DIR = os.path.join(os.getcwd(), "data", "chroma_db")

class ChromaVectorStore:
    def __init__(self, collection_name: str = "extension_rules"):
        # Garante que o diretório exista
        os.makedirs(DB_DIR, exist_ok=True)
        
        # Inicia o cliente persistente na pasta definida
        self.client = chromadb.PersistentClient(path=DB_DIR)
        
        # Cria ou obtém a coleção 
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"} # Métrica recomendada para similaridade semântica
        )

    def add_documents(self, chunks: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """Insere os blocos de texto no banco vetorial."""
        if not chunks:
            return
        
        # O ChromaDB cuida da criação de embeddings internamente (Default Embedding Function)
        self.collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        print(f"[{len(chunks)}] blocos indexados no ChromaDB.")

    def search(self, query: str, n_results: int = 4) -> List[Dict[str, Any]]:
        """Busca os blocos mais relevantes para a dúvida do aluno."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i]
                })
        return formatted_results

# Instância global (Singleton) para ser usada na aplicação
vector_db = ChromaVectorStore()