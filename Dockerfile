FROM python:3.12-slim
WORKDIR /app

# Instala as dependências:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o restante do código:
COPY . .

# Porta:
EXPOSE 8000

CMD ["uvicorn", "app:API", "--host", "0.0.0.0", "--port", "8000"]