import openai

# Imposta la tua API key OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_with_openai(audio_bytes):
    """
    Restituisce una lista di parole con timestamp:
    [
      { "word": "Come", "start": 0.12, "end": 0.35 },
      ...
    ]
    """
    response = openai.audio.transcriptions.create(
        model="gpt-4o-transcribe",
        file=("audio.wav", audio_bytes),
        response_format="verbose_json"
    )

    words = []

    # Estrae segmenti e parole con timestamp
    for segment in response.segments:
        for w in segment.words:
            words.append({
                "word": w.text,
                "start": w.start,
                "end": w.end
            })

    return words

