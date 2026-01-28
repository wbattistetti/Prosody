import subprocess
import tempfile

def convert_to_wav_pcm16(raw_bytes: bytes) -> bytes:
    # Salva input temporaneo (qualsiasi formato: mp3, wav, m4a, webm, ogg…)
    with tempfile.NamedTemporaryFile(delete=False) as tmp_in:
        tmp_in.write(raw_bytes)
        tmp_in_path = tmp_in.name

    # Output WAV temporaneo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_out:
        tmp_out_path = tmp_out.name

    # Conversione ffmpeg
    cmd = [
        "ffmpeg",
        "-y",
        "-i", tmp_in_path,     # ffmpeg capisce automaticamente il formato
        "-ac", "1",            # mono
        "-ar", "16000",        # 16kHz
        "-sample_fmt", "s16",  # PCM16
        tmp_out_path
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Leggi WAV convertito
    with open(tmp_out_path, "rb") as f:
        wav_bytes = f.read()

    return wav_bytes
