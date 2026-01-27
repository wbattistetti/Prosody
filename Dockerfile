# force rebuild
FROM python:3.10

WORKDIR /app

COPY MelodyExtractorServer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY MelodyExtractorServer/ .

# DICHIARA LA PORTA SU CUI UVICORN ASCOLTA
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
