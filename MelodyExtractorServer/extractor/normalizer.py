import numpy as np

def normalize_contours(pitch, energy):
    # Converti in numpy array
    pitch = np.array(pitch)
    energy = np.array(energy)

    # Lunghezza target uniforme
    target_len = 100

    # Interpolazione per normalizzare la lunghezza
    pitch_norm = np.interp(
        np.linspace(0, len(pitch) - 1, target_len),
        np.arange(len(pitch)),
        pitch
    )

    energy_norm = np.interp(
        np.linspace(0, len(energy) - 1, target_len),
        np.arange(len(energy)),
        energy
    )

    result = {
        "pitch_norm": pitch_norm.tolist(),
        "energy_norm": energy_norm.tolist()
    }

    # Debug per verificare cosa torna davvero
    print("DEBUG normalize_contours:", result)

    return result
