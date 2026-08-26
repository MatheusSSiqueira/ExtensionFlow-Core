import hashlib
from typing import List, Dict, Any, Tuple

def get_chunk_hash(text: str) -> str:
    """Gera um ID determinístico baseado no conteúdo para evitar duplicações no banco."""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def split_text_with_metadata(text: str, filename: str, chunk_size: int = 1500, overlap: int = 200) -> Tuple[List[str], List[Dict[str, Any]], List[str]]:
    """
    Divide o texto em blocos e anexa metadados (Source).
    Retorna: (chunks, metadatas, ids)
    """
    words = text.split()
    chunks = []
    metadatas = []
    ids = []

    if not words:
        return chunks, metadatas, ids

    i = 0
    while i < len(words):
        # Pegar um bloco de 'chunk_size' palavras
        chunk_words = words[i : i + chunk_size]
        chunk_text = " ".join(chunk_words).strip()
        
        if chunk_text:
            chunks.append(chunk_text)
            
            # Metadata dos documentos: O RAG deve preservar metadata
            metadatas.append({
                "source": filename,
                "document_type": "regulamento" if "regulamento" in filename.lower() else "anexo"
            })
            ids.append(get_chunk_hash(chunk_text))
            
        # Avançar respeitando o overlap (sobreposição de contexto)
        i += chunk_size - overlap

    return chunks, metadatas, ids