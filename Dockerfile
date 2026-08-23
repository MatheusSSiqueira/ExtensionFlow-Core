# Usa uma versão oficial e leve do Python
FROM python:3.11-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para dentro do container
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# O comando que o container vai rodar quando ligar
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]