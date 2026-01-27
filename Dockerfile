FROM python:3.10

WORKDIR /app

# Copia il requirements.txt dalla ROOT
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia TUTTO il progetto dentro /app
COPY . .

# Avvia uvicorn puntando a main.py nella root
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


