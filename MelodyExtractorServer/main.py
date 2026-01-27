from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import io
import soundfile as sf
import tempfile
import torch
import whisperx

from MelodyExtractorServer.extractor.pitch_analyzer import extract_pitch
from MelodyExtractorServer.extractor.energy_analyzer import extract_energy
from MelodyExtractorServer.extractor.rhythm_analyzer import extract_rhythm
from MelodyExtractorServer.extractor.pause_detector import extract_pauses
from MelodyExtractorServer.extractor.normalizer import normalize_contours
from MelodyExtractorServer.utils.response_builder import build_response

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
# WHISPERX: CARICAMENTO MODELLO UNA SOLA VOLTA
# -----------------------------------------------------

device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    whisper_model = whisperx.load_model("medium", device)
except Exception as e:
    print("Errore nel caricamento WhisperX:", e)
    whisper_model = None

# -----------------------------------------------------
# ENDPOINT /transcribe (WhisperX)
# -----------------------------------------------------

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    if whisper_model is None:
        raise HTTPException(status_code=500, detail="WhisperX non è stato caricato")

    # Salva file temporaneo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name

    # Trascrizione
    result = whisper_model.transcribe(tmp_path)

    # Alignment
    model_a, metadata = whisperx.load_align_model(
        language_code=result["language"], device=device
    )
    aligned = whisperx.align(
        result["segments"], model_a, metadata, tmp_path, device
    )

    return {
        "text": result["text"],
        "words": aligned["word_segments"]
    }

# -----------------------------------------------------
# ENDPOINT /extract-prosody (il tuo già esistente)
# -----------------------------------------------------

@app.post("/extract-prosody")
def extract_prosody(request: AudioRequest):
    try:
        # Decodifica audio base64
        audio_bytes = base64.b64decode(request.audio_base64)
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
