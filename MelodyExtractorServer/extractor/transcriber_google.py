import os
import json
from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech

def transcribe_with_google(audio_bytes):
    creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_json:
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS env var is missing")

    creds_dict = json.loads(creds_json)
    credentials = service_account.Credentials.from_service_account_info(creds_dict)
    client = speech.SpeechClient(credentials=credentials)

    audio = speech.RecognitionAudio(content=audio_bytes)

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

    # ⭐ QUI: long running
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=90)

    words = []

    for result in response.results:
        if not result.alternatives:
            continue

        alternative = result.alternatives[0]

        if not alternative.words:
            continue

        for w in alternative.words:
            words.append({
                "word": w.word,
                "start": w.start_time.total_seconds(),
                "end": w.end_time.total_seconds()
            })

    return words
