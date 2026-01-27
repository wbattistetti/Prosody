from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import io
import soundfile as sf

from extractor.pitch_analyzer import extract_pitch
from extractor.energy_analyzer import extract_energy
from extractor.rhythm_analyzer import extract_rhythm
from extractor.pause_detector import extract_pauses
from extractor.normalizer import normalize_contours

from utils.response_builder import build_response

app = FastAPI()

# ---------------------------
# MODELLI
# ---------------------------

class AudioRequest(BaseModel):
    audio_base64: str
    sample_rate: int = 16000


# ---------------------------
# ENDPOINT DI SERVIZIO
# ---------------------------

@app.get("/")
def root():
    return {"status": "ok", "message": "Server running"}


@app.get("/favicon.ico")
def favicon():
    return {}


# ---------------------------
# ENDPOINT PRINCIPALE
# ---------------------------

@app.post("/analyze")
def analyze_audio(request: AudioRequest):
    try:
        # Decodifica Base64
        audio_bytes = base64.b64decode(request.audio_base64)
        audio_buffer = io.BytesIO(audio_bytes)

        # Caricamento audio
        audio_data, sr = sf.read(audio_buffer)

        # Estrazioni
        pitch = extract_pitch(audio_data, sr)
        energy = extract_energy(audio_data, sr)
        rhythm = extract_rhythm(audio_data, sr)
        pauses = extract_pauses(audio_data, sr)

        # Normalizzazione
        normalized = normalize_contours(pitch, energy, rhythm)

        # Risposta finale
        return build_response(
            pitch=normalized["pitch"],
            energy=normalized["energy"],
            rhythm=normalized["rhythm"],
            pauses=pauses
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
