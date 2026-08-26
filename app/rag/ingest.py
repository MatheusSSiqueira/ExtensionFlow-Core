import os
from app.rag.loaders import extract_document_text
from app.rag.splitter import split_text_with_metadata
from app.rag.vector_store import vector_db

RAW_DOCS_DIR = os.path.join(os.getcwd(), "data", "raw_docs")

def build_vector_database():
    """Varrer diretório de dados brutos recursivamente e ingerir todos os documentos suportados."""
    if not os.path.exists(RAW_DOCS_DIR):
        print(f"Diretório {RAW_DOCS_DIR} não encontrado.")
        return

    print("=== Iniciando Ingestão de Documentos ===")
    arquivos_processados = 0
    
    # os.walk permite ler arquivos dentro de subpastas
    for root, _, files in os.walk(RAW_DOCS_DIR):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Ignora arquivos de sistema ou ocultos
            if filename.startswith('.'):
                continue
                
            print(f"Lendo: {filename}...")
            text_content = extract_document_text(file_path)
            
            if not text_content:
                continue
                
            # Divide e injeta metadados
            chunks, metadatas, ids = split_text_with_metadata(text_content, filename)
            
            # Salva no banco (O hash evita criar clones)
            vector_db.add_documents(chunks, metadatas, ids)
            arquivos_processados += 1
            
    print(f"=== Processo de Ingestão Concluído. {arquivos_processados} arquivos processados. ===")

if __name__ == "__main__":
    build_vector_database()