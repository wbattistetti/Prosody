import os
import io

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import soundfile as sf
import numpy as np

from MelodyExtractorServer.extractor.converter import convert_to_linear16
from MelodyExtractorServer.extractor.pitch_analyzer import extract_pitch
from MelodyExtractorServer.extractor.energy_analyzer import extract_energy
from MelodyExtractorServer.extractor.rhythm_analyzer import extract_rhythm
from MelodyExtractorServer.extractor.pause_detector import extract_pauses
from MelodyExtractorServer.extractor.normalizer import normalize_contours

# 👉 Labeling prosodico
from MelodyExtractorServer.extractor.labeling import assign_labels

# 👉 Trascrizione con Google STT
from MelodyExtractorServer.extractor.transcriber_google import transcribe_with_google

from MelodyExtractorServer.utils.response_builder import build_response


# ---------------------------------------------------------
# UTIL: conversione in tipi JSON-serializzabili
# ---------------------------------------------------------

def to_jsonable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    if isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    if isinstance(obj, dict):
        return {k: to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_jsonable(x) for x in obj]
    return obj


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
# ENDPOINT DI ESTRAZIONE
# ---------------------------------------------------------

@app.post("/extractor")
async def extractor(file: UploadFile = File(...)):
    try:
        # Carica audio
        audio_bytes = await file.read()
        audio_bytes = convert_to_linear16(audio_bytes)

        print("DEBUG after conversion:", len(audio_bytes))
        audio_data, sr = sf.read(io.BytesIO(audio_bytes))
        print("DEBUG shape:", audio_data.shape, "sr:", sr)

        # 👉 Trascrizione con timestamp (Google)
        words = transcribe_with_google(audio_bytes)

        # Estrai feature prosodiche
        pitch = extract_pitch(audio_data, sr)
        energy = extract_energy(audio_data, sr)
        rhythm = extract_rhythm(audio_data, sr)
        pauses = extract_pauses(audio_data, sr)

        # Normalizza
        normalized = normalize_contours(pitch, energy)

        # 👉 Genera etichette prosodiche
        labels = assign_labels(
            pitch=normalized["pitch"],
            energy=normalized["energy"],
            pauses=pauses
        )

        # Costruisci risposta (tutto JSON-safe)
        response = {
            "success": True,
            "data": {
                "pitch": to_jsonable(normalized["pitch"]),
                "energy": to_jsonable(normalized["energy"]),
                "rhythm": to_jsonable(rhythm),
                "pauses": to_jsonable(pauses),
                "normalized": to_jsonable(normalized),
                "labels": to_jsonable(labels),
                "words": to_jsonable(words),
            },
        }

        print(
            "DEBUG types:",
            type(normalized["pitch"]),
            type(normalized["energy"]),
            type(rhythm),
            type(pauses),
            type(labels),
            type(words),
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
