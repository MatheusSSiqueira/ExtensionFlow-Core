import os
from app.rag.vector_store import vector_db

def load_and_index_document():
    file_path = "data/raw_docs/regulamento_extensao.txt"
    
    # 1. Lê o arquivo
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 2. Divide o texto em trechos (chunks) separando pelos parágrafos duplos
    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
    
    # 3. Prepara os IDs únicos e Metadados 
    ids = [f"reg_{i}" for i in range(len(chunks))]
    metadatas = [{"source": "regulamento_extensao.txt"} for _ in chunks]
    
    # 4. Envia para o banco de dados 
    print(f"Iniciando a ingestão de {len(chunks)} trechos no banco de dados...")
    vector_db.add_chunks(chunks, metadatas, ids)
    print("Sucesso! Documentos vetorizados e salvos no ChromaDB.")

# Para rodar o script diretamente
if __name__ == "__main__":
    # Garante que as pastas existam para não dar erro
    os.makedirs("data/raw_docs", exist_ok=True)
    load_and_index_document()