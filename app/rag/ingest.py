import os
from app.rag.vector_store import vector_db

def load_and_index_documents():
    """
    Pipeline oficial de ingestão.
    Lê todos os arquivos de texto do diretório e os envia para o banco vetorial.
    """
    docs_dir = "data/raw_docs"
    
    # Verifica se a pasta existe
    if not os.path.exists(docs_dir):
        print(f"Diretório '{docs_dir}' não encontrado. Crie a pasta e adicione os regulamentos.")
        return

    arquivos_encontrados = [f for f in os.listdir(docs_dir) if f.endswith(".txt")]
    
    if not arquivos_encontrados:
        print("Nenhum documento .txt encontrado para ingestão.")
        return

    for filename in arquivos_encontrados:
        file_path = os.path.join(docs_dir, filename)
        
        # 1. Lê o documento de forma genérica
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 2. Divide em chunks
        chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
        
        # 3. Cria IDs e Metadados dinâmicos baseados no nome do arquivo 
        ids = [f"{filename.replace('.txt', '')}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": filename} for _ in chunks]
        
        # 4. Salva no ChromaDB
        print(f"Vetorizando {len(chunks)} regras do documento: {filename}...")
        vector_db.add_chunks(chunks, metadatas, ids)
        
    print("Processo de indexação concluído com sucesso!")

if __name__ == "__main__":
    load_and_index_documents()