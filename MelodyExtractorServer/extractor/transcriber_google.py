import os
import json
from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech

def transcribe_with_google(audio_bytes):
    print("\n================ GOOGLE STT DEBUG ================")

    # 1. Carica credenziali
    creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_json:
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS env var is missing")

    print("DEBUG: Credenziali trovate (lunghezza JSON):", len(creds_json))

    creds_dict = json.loads(creds_json)
    credentials = service_account.Credentials.from_service_account_info(creds_dict)
    client = speech.SpeechClient(credentials=credentials)

    # 2. Prepara audio
    print("DEBUG: Bytes audio ricevuti:", len(audio_bytes))
    audio = speech.RecognitionAudio(content=audio_bytes)

    # 3. Configurazione
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="it-IT",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
        audio_channel_count=1,
        use_enhanced=True,
        model="default"
    )

    print("DEBUG: Config STT pronta")

    # 4. Chiamata long-running
    print("DEBUG: Avvio long_running_recognize()...")
    operation = client.long_running_recognize(config=config, audio=audio)

    print("DEBUG: Attendo risultato...")
    response = operation.result(timeout=90)

    print("DEBUG: Risposta ricevuta da Google")
    print("DEBUG: Numero risultati:", len(response.results))

    words = []

    # 5. Analisi risultati
    for i, result in enumerate(response.results):
        print(f"\n--- RESULT {i} ---")
        print("DEBUG: Numero alternative:", len(result.alternatives))

        if not result.alternatives:
            print("DEBUG: Nessuna alternativa → skip")
            continue

        alternative = result.alternatives[0]

        print("DEBUG: Transcript:", alternative.transcript)
        print("DEBUG: Confidence:", alternative.confidence)

        if not alternative.words:
            print("DEBUG: alternative.words è VUOTO o NONE")
            continue

        print("DEBUG: Numero parole:", len(alternative.words))

        for w in alternative.words:
            words.append({
                "word": w.word,
                "start": w.start_time.total_seconds(),
                "end": w.end_time.total_seconds()
            })

    print("DEBUG: Parole estratte:", len(words))
    print("=================================================\n")

    return words
