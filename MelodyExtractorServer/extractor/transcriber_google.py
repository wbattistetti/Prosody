import os
import json
from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech

def transcribe_with_google(audio_bytes):
    # 1. Carica il JSON delle credenziali dalla variabile d'ambiente
    creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_json:
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS env var is missing")

    # 2. Converte la stringa JSON in dict
    creds_dict = json.loads(creds_json)

    # 3. Crea le credenziali Google
    credentials = service_account.Credentials.from_service_account_info(creds_dict)

    # 4. Inizializza il client STT
    client = speech.SpeechClient(credentials=credentials)

    # 5. Prepara l’audio
    audio = speech.RecognitionAudio(content=audio_bytes)

    # 6. Configura la trascrizione con timestamp parola-per-parola
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="it-IT",
        enable_word_time_offsets=True
    )

    # 7. Esegue la trascrizione
    response = client.recognize(config=config, audio=audio)

    # 8. Estrae le parole con timestamp
    words = []
    for result in response.results:
        alternative = result.alternatives[0]
        for w in alternative.words:
            words.append({
                "word": w.word,
                "start": w.start_time.total_seconds(),
                "end": w.end_time.total_seconds()
            })

    return words
