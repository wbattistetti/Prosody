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
        print("DEBUG extract_pitch (no voiced frames): contour vuoto")
        return np.array([])

    # Normalizzazione del contour
    contour = (values - values.min()) / (values.max() - values.min() + 1e-6)

    # Debug per verificare cosa torna davvero
    print("DEBUG extract_pitch — contour length:", len(contour))

    # Restituiamo SOLO il contour (array/lista), come per energy
    return contour
