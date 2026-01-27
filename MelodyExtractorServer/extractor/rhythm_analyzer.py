import librosa

def extract_rhythm(audio, sr):
    onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    speaking_rate = len(beats) / (len(audio) / sr)

    return {
        "speaking_rate": float(speaking_rate),
        "tempo": float(tempo),
        "accents": beats.tolist()
    }
