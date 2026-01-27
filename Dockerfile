# force rebuild
FROM python:3.10

WORKDIR /app

# Copia tutto il progetto (inclusa la cartella MelodyExtractorServer)
COPY . .

# Installa le dipendenze dal percorso corretto
RUN pip install --no-cache-dir -r MelodyExtractorServer/requirements.txt

# Espone la porta su cui Uvicorn ascolta
EXPOSE 8000

# Avvia FastAPI dal percorso corretto
CMD ["uvicorn", "MelodyExtractorServer.main:app", "--host", "0.0.0.0", "--port", "8000"]
