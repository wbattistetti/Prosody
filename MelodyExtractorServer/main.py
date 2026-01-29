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
        # DEBUG: cosa arriva dal frontend 
        print("DEBUG RAW REQUEST:", request) 
        print("DEBUG BASE64 TYPE:", type(request.audio_base64))
        
        # 1. Decodifica base64
        raw_bytes = base64.b64decode(request.audio_base64)

        # 2. Conversione robusta in WAV PCM16 16kHz mono
        wav_bytes = convert_to_wav_pcm16(raw_bytes)

        # 3. Caricamento WAV convertito
        audio_data, sr = sf.read(io.BytesIO(wav_bytes))

        # 4. Estrazione feature
        pitch = extract_pitch(audio_data, sr)
        print("DEBUG PITCH:", pitch)

        energy = extract_energy(audio_data, sr)
        print("DEBUG ENERGY:", energy)

        rhythm = extract_rhythm(audio_data, sr)
        print("DEBUG RHYTHM:", rhythm)

        pauses = extract_pauses(audio_data, sr)
        print("DEBUG PAUSES:", pauses)

        # 5. Normalizzazione
        normalized = normalize_contours(
            pitch=pitch["contour"],
            energy=energy["contour"]
        )
        print("DEBUG NORMALIZED:", normalized)

        # 6. Costruzione risposta
        response = build_response(
            pitch=pitch,
            energy=energy,
            rhythm=rhythm,
            pauses=pauses,
            normalized=normalized,
            duration=len(audio_data) / sr,
            sr=sr
        )

        print("DEBUG RESPONSE:", response)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



