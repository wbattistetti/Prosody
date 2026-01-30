import librosa
import numpy as np

def extract_energy(audio, sr):
    # Calcolo RMS frame-by-frame
    rms = librosa.feature.rms(y=audio)[0]

    # Normalizzazione del contour
    contour = (rms - rms.min()) / (rms.max() - rms.min() + 1e-6)

    # Debug utile
    print("DEBUG extract_energy — contour length:", len(contour))

    # Restituiamo SOLO il contour, come per il pitch
    return contour
