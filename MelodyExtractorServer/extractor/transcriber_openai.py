import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_with_openai(audio_bytes):
    """
    Restituisce una lista di parole con timestamp:
    [
      { "word": "Come", "start": 0.12, "end": 0.35 },
      ...
    ]
    """

    response = client.audio.transcriptions.create(
        model="gpt-4o-transcribe",
        file=("audio.wav", audio_bytes),
        response_format="json"   # <-- CORRETTO
    )

    words = []

    # Il nuovo formato ha response["segments"]
    for segment in response["segments"]:
        for w in segment["words"]:
            words.append({
                "word": w["text"],
                "start": w["start"],
                "end": w["end"]
            })

    return words

