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

class AudioRequest(BaseModel):
    audio_base64: str
    sample_rate: int = 16000

@app.post("/extract")
def extract_prosody(req: AudioRequest):
    try:
        audio_bytes = base64.b64decode(req.audio_base64)
        audio, sr = sf.read(io.BytesIO(audio_bytes))

        if len(audio) < sr * 0.5:
            raise HTTPException(status_code=400, detail="Audio too short")

        pitch_data = extract_pitch(audio, sr)
        energy_data = extract_energy(audio, sr)
        rhythm_data = extract_rhythm(audio, sr)
        pauses = extract_pauses(audio, sr)

        normalized = normalize_contours(
            pitch_data["contour"],
            energy_data["contour"]
        )

        return build_response(
            pitch_data,
            energy_data,
            rhythm_data,
            pauses,
            normalized,
            len(audio) / sr,
            sr
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
