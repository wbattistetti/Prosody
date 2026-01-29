# MelodyExtractorServer/extractor/transcriber.py

import whisper_timestamped as whisper

# Carichiamo il modello una sola volta (versione base per iniziare)
model = whisper.load_model("base")

def transcribe_with_timestamps(audio_data, sr):
    """
    Ritorna una lista di parole con start/end in secondi:
    [
      { "word": "Come", "start": 0.10, "end": 0.35 },
      ...
    ]
    """
    # whisper-timestamped vuole un file o un array + sample rate
    # Convertiamo in formato atteso
    result = whisper.transcribe(model, audio_data, sample_rate=sr)

    words = []
    for segment in result["segments"]:
        for w in segment["words"]:
            words.append({
                "word": w["text"].strip(),
                "start": w["start"],
                "end": w["end"]
            })

    return words
