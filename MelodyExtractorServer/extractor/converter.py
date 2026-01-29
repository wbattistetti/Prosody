# converter.py
import io
from pydub import AudioSegment

def convert_to_linear16(audio_bytes: bytes) -> bytes:
    """
    Converte qualsiasi audio in LINEAR16 16kHz mono,
    il formato richiesto da Google Speech-to-Text.
    """

    # Carica l'audio da bytes (pydub riconosce automaticamente il formato)
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

    # Conversione standardizzata
    audio = (
        audio.set_frame_rate(16000)   # 16 kHz
             .set_channels(1)         # mono
             .set_sample_width(2)     # 16-bit PCM
    )

    # Ritorna i raw bytes (LINEAR16)
    return audio.raw_data
