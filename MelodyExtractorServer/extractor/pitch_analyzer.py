import parselmouth
import numpy as np

def extract_pitch(audio, sr):
    snd = parselmouth.Sound(audio, sampling_frequency=sr)
    pitch = snd.to_pitch(time_step=0.01)
    values = pitch.selected_array['frequency']
    values = values[values > 0]

    contour = (values - values.min()) / (values.max() - values.min() + 1e-6)

    return {
        "min": float(values.min()),
        "max": float(values.max()),
        "mean": float(values.mean()),
        "contour": contour.tolist()
    }
