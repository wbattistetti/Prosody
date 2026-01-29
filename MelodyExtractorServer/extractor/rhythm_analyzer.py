import librosa

def extract_rhythm(audio, sr):
    # Calcolo dell'onset envelope
    onset_env = librosa.onset.onset_strength(y=audio, sr=sr)

    # Estrazione tempo e battiti
    tempo, beats = librosa.beat.beat_track(
        onset_envelope=onset_env,
        sr=sr
    )

    # Speaking rate = numero di accenti per secondo
    duration_seconds = len(audio) / sr
    speaking_rate = len(beats) / duration_seconds if duration_seconds > 0 else 0.0

    result = {
        "speaking_rate": float(speaking_rate),
        "tempo": float(tempo),
        "accents": beats.tolist()
    }

    # Debug per verificare cosa torna davvero
    print("DEBUG extract_rhythm:", result)

    return result
