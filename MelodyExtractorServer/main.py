from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import io
import soundfile as sf

from MelodyExtractorServer.extractor.pitch_analyzer import extract_pitch
from MelodyExtractorServer.extractor.energy_analyzer import extract_energy
from MelodyExtractorServer.extractor.rhythm_analyzer import extract_rhythm
from MelodyExtractorServer.extractor.pause_detector import extract_pauses
from MelodyExtractorServer.extractor.normalizer import normalize_contours

from MelodyExtractorServer.utils.response_builder import build_response


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
# ENDPOINT DI ESTRAZIONE (VERSIONE CORRETTA PER multipart/form-data)
# ---------------------------------------------------------

@app.post("/extract")
async def extract_audio_features(file: UploadFile = File(...)):
    try:
        # 1. Leggi i byte del file WAV inviato dal frontend
        wav_bytes = await file.read()

        # 2. Carica l’audio in memoria
        audio_data, sr = sf.read(io.BytesIO(wav_bytes))

        # 3. Estrazione delle feature
        pitch = extract_pitch(audio_data, sr)
        print("DEBUG PITCH:", pitch)

        energy = extract_energy(audio_data, sr)
        print("DEBUG ENERGY:", energy)

        rhythm = extract_rhythm(audio_data, sr)
        print("DEBUG RHYTHM:", rhythm)

        pauses = extract_pauses(audio_data, sr)
        print("DEBUG PAUSES:", pauses)

        # 4. Normalizzazione
        normalized = normalize_contours(
            pitch=pitch["contour"],
            energy=energy["contour"]
        )
        print("DEBUG NORMALIZED:", normalized)

        # 5. Costruzione risposta finale
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
