import librosa
import numpy as np

def extract_energy(audio, sr):
    rms = librosa.feature.rms(y=audio)[0]
    contour = (rms - rms.min()) / (rms.max() - rms.min() + 1e-6)

    return {
        "mean": float(rms.mean()),
        "contour": contour.tolist()
    }
