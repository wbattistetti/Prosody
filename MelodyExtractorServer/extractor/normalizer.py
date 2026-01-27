import numpy as np

def normalize_contours(pitch, energy):
    pitch = np.array(pitch)
    energy = np.array(energy)

    target_len = 100
    pitch_norm = np.interp(np.linspace(0, len(pitch)-1, target_len), np.arange(len(pitch)), pitch)
    energy_norm = np.interp(np.linspace(0, len(energy)-1, target_len), np.arange(len(energy)), energy)

    return {
        "pitch_norm": pitch_norm.tolist(),
        "energy_norm": energy_norm.tolist()
    }
