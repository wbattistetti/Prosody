import tempfile
import subprocess
import os

def convert_to_wav_pcm16(audio_bytes: bytes) -> bytes:
    """
    Converte QUALSIASI file audio in WAV PCM 16-bit, mono, 16kHz.
    Restituisce i bytes del file convertito.
    """

    # 1. Salva il file originale in un file temporaneo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".input") as f_in:
        f_in.write(audio_bytes)
        input_path = f_in.name

    # 2. Crea un file temporaneo per l'output WAV convertito
    output_path = input_path + "_converted.wav"

    # 3. Comando ffmpeg per convertire tutto in WAV PCM 16kHz mono
    cmd = [
        "ffmpeg",
        "-y",                # sovrascrivi senza chiedere
        "-i", input_path,    # input
        "-ac", "1",          # mono
        "-ar", "16000",      # 16kHz
        "-sample_fmt", "s16",# PCM 16-bit
        output_path
    ]

    # 4. Esegui ffmpeg
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 5. Leggi il file convertito
    with open(output_path, "rb") as f_out:
        converted_bytes = f_out.read()

    # 6. Pulisci i file temporanei
    os.remove(input_path)
    os.remove(output_path)

    return converted_bytes
