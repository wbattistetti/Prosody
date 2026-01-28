from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import io
import soundfile as sf

from MelodyExtractorServer.extractor.pitch_analyzer import extract_pitch
from MelodyExtractorServer.extractor.energy_analyzer import extract_energy
from MelodyExtractorServer.extractor.rhythm_analyzer import extract_rhythm
from MelodyExtractorServer.extractor.pause_detector import extract_pauses
from MelodyExtractorServer.extractor.normalizer import normalize_contours
from MelodyExtractorServer.utils.response_builder import build_response
from MelodyExtractorServer.utils.audio_utils import convert_to_wav_pcm16

# -----------------------------------------------------
# APP + CORS
# -----------------------------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ok per test
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------
# MODELLI
# -----------------------------------------------------

class AudioRequest(BaseModel):
    audio_base64: str
    sample_rate: int = 16000

# -----------------------------------------------------
# ENDPOINT DI SERVIZIO
# -----------------------------------------------------

@app.get("/")
def root():
    return {"status": "ok", "message": "Server running"}

@app.get("/favicon.ico")
def favicon():
    return {}

# -----------------------------------------------------
# ENDPOINT /extract-prosody
# (UNICO ENDPOINT CHE DEVE STARE SU RAILWAY)
# -----------------------------------------------------

@app.post("/extract-prosody")
def extract_prosody(request: AudioRequest):
    try:
        # Decodifica audio base64
        print("=== DEBUG SERVER ===") 
        print("Base64 length:", len(request.audio_base64)) 
        audio_bytes = base64.b64decode(request.audio_base64) 
        print("Decoded bytes:", len(audio_bytes)) 
        print("First 32 bytes:", audio_bytes[:32])
        
        audio_io = io.BytesIO(audio_bytes)
        audio_data, sr = sf.read(audio_io)

        # Estrazione feature
        pitch = extract_pitch(audio_data, sr)
        energy = extract_energy(audio_data, sr)
        rhythm = extract_rhythm(audio_data, sr)
        pauses = extract_pauses(audio_data, sr)

        # Normalizzazione
        pitch_norm, energy_norm = normalize_contours(pitch, energy)

        # Risposta finale
        response = build_response(
            pitch_norm,
            energy_norm,
            rhythm,
            pauses,
            sr
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-prosody")
def extract_prosody(request: AudioRequest):
    try:
        # 1. Decodifica base64
        raw_bytes = base64.b64decode(request.audio_base64)

        # 2. Conversione robusta in WAV PCM 16kHz mono
        wav_bytes = convert_to_wav_pcm16(raw_bytes)

        # 3. Carica il WAV convertito
        audio_data, sr = sf.read(io.BytesIO(wav_bytes))

        # 4. Analisi prosodica
        pitch = extract_pitch(audio_data, sr)
        energy = extract_energy(audio_data, sr)
        rhythm = extract_rhythm(audio_data, sr)
        pauses = extract_pauses(audio_data, sr)

        # 5. Normalizzazione
        normalized = normalize_contours(
            pitch=pitch,
            energy=energy,
            rhythm=rhythm,
            pauses=pauses
        )

        # 6. Risposta finale
        return build_response(normalized)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



