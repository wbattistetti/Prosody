from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

# ---------------------------------------------------------
# APP SETUP
# ---------------------------------------------------------

app = FastAPI()

# CORS (fondamentale per permettere a Prosody di chiamare l’API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # puoi restringerlo in futuro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# REQUEST MODEL
# ---------------------------------------------------------

class AudioRequest(BaseModel):
    audio_base64: str
    sample_rate: int = 16000

# ---------------------------------------------------------
# ENDPOINT DI ESTRAZIONE
# ---------------------------------------------------------

@app.post("/extract")
async def extract_audio_features(request: AudioRequest):
    try:
        # Decodifica base64
        audio_bytes = base64.b64decode(request.audio_base64)
        audio_buffer = io.BytesIO(audio_bytes)

        # Carica audio
        audio_data, sr = sf.read(audio_buffer)
        if sr != request.sample_rate:
            raise HTTPException(status_code=400, detail="Sample rate mismatch")

        # Estrazioni
        pitch = extract_pitch(audio_data, sr)
        energy = extract_energy(audio_data, sr)
        rhythm = extract_rhythm(audio_data, sr)
        pauses = extract_pauses(audio_data, sr)

        # Normalizzazione
        normalized = normalize_contours(pitch, energy, rhythm)

        # Costruzione risposta
        response = build_response(
            pitch=normalized["pitch"],
            energy=normalized["energy"],
            rhythm=normalized["rhythm"],
            pauses=pauses
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
