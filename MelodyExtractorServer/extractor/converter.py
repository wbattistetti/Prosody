# converter.py
import io
import soundfile as sf
import numpy as np

def convert_to_linear16(audio_bytes: bytes) -> bytes:
    # 1. Leggi l'audio originale (DEVE essere WAV)
    data, sr = sf.read(io.BytesIO(audio_bytes), dtype='int16')

    # 2. Stereo → mono
    if len(data.shape) == 2:
        data = data.mean(axis=1).astype(np.int16)

    # 3. Risampling se necessario
    if sr != 16000:
        duration = len(data) / sr
        new_length = int(duration * 16000)
        data = np.interp(
            np.linspace(0, len(data), new_length),
            np.arange(len(data)),
            data
        ).astype(np.int16)

    # 4. Ricostruisci un WAV valido
    buffer = io.BytesIO()
    sf.write(buffer, data, 16000, format='WAV', subtype='PCM_16')

    return buffer.getvalue()
