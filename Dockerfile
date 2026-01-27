FROM python:3.10

WORKDIR /app

# Copia SOLO requirements dalla cartella MelodyExtractorServer
COPY MelodyExtractorServer/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia TUTTO il contenuto di MelodyExtractorServer dentro /app
COPY MelodyExtractorServer/ .

# Avvia uvicorn puntando a main.py che ora è in /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

