import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_with_openai(audio_bytes):
    response = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=("audio.wav", audio_bytes),
        response_format="json",
        timestamp_granularities=["word"]
    )

    words = []

    for segment in response.segments:
        for w in segment.words:
            words.append({
                "word": w.text,
                "start": w.start,
                "end": w.end
            })

    return words

