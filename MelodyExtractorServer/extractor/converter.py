# converter.py
import io
import soundfile as sf
import numpy as np

def convert_to_linear16(audio_bytes: bytes) -> bytes:
    # Leggi l'audio con soundfile (supporta WAV nativamente)
    data, sr = sf.read(io.BytesIO(audio_bytes), dtype='int16')

    # Se stereo → converti in mono
    if len(data.shape) == 2:
        data = data.mean(axis=1).astype(np.int16)

    # Se sample rate ≠ 16000 → risampling semplice
    if sr != 16000:
        # Calcolo del nuovo numero di campioni
        duration = len(data) / sr
        new_length = int(duration * 16000)
        data = np.interp(
            np.linspace(0, len(data), new_length),
            np.arange(len(data)),
            data
        ).astype(np.int16)

    # Ritorna i raw bytes LINEAR16
    return data.tobytes()
