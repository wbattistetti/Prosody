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
from utils.audio_utils import convert_to_wav_pcm16   # <-- AGGIUNTO

# ---------------------------------------------------------
# APP SETUP
# ---------------------------------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        # 1. Decodifica base64
        raw_bytes = base64.b64decode(request.audio_base64)

        # 2. Conversione robusta in WAV PCM16 16kHz mono
        wav_bytes = convert_to_wav_pcm16(raw_bytes)

        # 3. Caricamento WAV convertito
        audio_data, sr = sf.read(io.BytesIO(wav_bytes))

        # 4. Estrazione feature
        pitch = extract_pitch(audio_data, sr)
        energy = extract_energy(audio_data, sr)
        rhythm = extract_rhythm(audio_data, sr)
        pauses = extract_pauses(audio_data, sr)

        # 5. Normalizzazione
        normalized = normalize_contours(
            pitch=pitch,
            energy=energy,
            rhythm=rhythm
        )

        # 6. Costruzione risposta
        response = build_response(
            pitch=normalized["pitch"],
            energy=normalized["energy"],
            rhythm=normalized["rhythm"],
            pauses=pauses
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
