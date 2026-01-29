import parselmouth
import numpy as np

def extract_pitch(audio, sr):
    # Creazione oggetto Parselmouth
    snd = parselmouth.Sound(audio, sampling_frequency=sr)

    # Estrazione pitch con step di 10ms
    pitch = snd.to_pitch(time_step=0.01)

    # Array delle frequenze
    values = pitch.selected_array['frequency']

    # Filtra valori non validi (0 = non voce)
    values = values[values > 0]

    # Evita crash se non c'è voce
    if len(values) == 0:
        result = {
            "min": 0.0,
            "max": 0.0,
            "mean": 0.0,
            "contour": []
        }
        print("DEBUG extract_pitch (no voiced frames):", result)
        return result

    # Normalizzazione del contour
    contour = (values - values.min()) / (values.max() - values.min() + 1e-6)

    result = {
        "min": float(values.min()),
        "max": float(values.max()),
        "mean": float(values.mean()),
        "contour": contour.tolist()
    }

    # Debug per verificare cosa torna davvero
    print("DEBUG extract_pitch:", result)

    return result
