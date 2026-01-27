# force rebuild
FROM python:3.10

WORKDIR /app

# Copia tutto il progetto
COPY . .

# Installa le dipendenze
RUN pip install --no-cache-dir -r MelodyExtractorServer/requirements.txt

# Espone la porta
EXPOSE 8000

# Avvia FastAPI dal percorso corretto
CMD ["uvicorn", "MelodyExtractorServer.main:app", "--host", "0.0.0.0", "--port", "8000"]
