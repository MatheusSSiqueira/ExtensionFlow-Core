import os
from pypdf import PdfReader
from docx import Document as DocxReader

def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def load_pdf(file_path: str) -> str:
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e:
        print(f"Erro ao ler PDF {file_path}: {e}")
    return text

def load_docx(file_path: str) -> str:
    text = ""
    try:
        doc = DocxReader(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
        # Lê tabelas, importante para a "Ficha de Frequência"
        for table in doc.tables:
            for row in table.rows:
                row_data = [cell.text for cell in row.cells]
                text += " | ".join(row_data) + "\n"
    except Exception as e:
        print(f"Erro ao ler DOCX {file_path}: {e}")
    return text

def extract_document_text(file_path: str) -> str:
    """Roteia o arquivo para o leitor correto com base na extensão."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        return load_txt(file_path)
    elif ext == ".pdf":
        return load_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        return load_docx(file_path)
    else:
        print(f"Formato não suportado ignorado: {file_path}")
        return ""