import librosa
import numpy as np

def extract_energy(audio, sr):
    # Calcolo RMS
    rms = librosa.feature.rms(y=audio)[0]

    # Normalizzazione del contour
    contour = (rms - rms.min()) / (rms.max() - rms.min() + 1e-6)

    result = {
        "mean": float(rms.mean()),
        "contour": contour.tolist()
    }

    # Debug utile per capire cosa torna davvero
    print("DEBUG extract_energy:", result)

    return result
