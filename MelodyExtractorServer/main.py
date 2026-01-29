from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import io
import soundfile as sf

from MelodyExtractorServer.extractor.pitch_analyzer import extract_pitch
from MelodyExtractorServer.extractor.energy_analyzer import extract_energy
from MelodyExtractorServer.extractor.rhythm_analyzer import extract_rhythm
from MelodyExtractorServer.extractor.pause_detector import extract_pauses
from MelodyExtractorServer.extractor.normalizer import normalize_contours

# 👉 AGGIUNTA: import del nuovo modulo di labeling
from MelodyExtractorServer.extractor.labeling import assign_labels

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

@app.post("/extractor")
async def extractor(file: UploadFile = File(...)):
    try:
        # Carica audio
        audio_bytes = await file.read()
        audio_data, sr = sf.read(io.BytesIO(audio_bytes))

        # Estrai feature prosodiche
        pitch = extract_pitch(audio_data, sr)
        energy = extract_energy(audio_data, sr)
        rhythm = extract_rhythm(audio_data, sr)
        pauses = extract_pauses(audio_data, sr)

        # Normalizza
        normalized = normalize_contours(pitch, energy)

        # 👉 AGGIUNTA: genera etichette prosodiche discrete
        labels = assign_labels(
            pitch=normalized["pitch"],
            energy=normalized["energy"],
            pauses=pauses
        )

        # Costruisci risposta
        response = {
            "success": True,
            "data": {
                "pitch": normalized["pitch"],
                "energy": normalized["energy"],
                "rhythm": rhythm,
                "pauses": pauses,
                "normalized": normalized,
                # 👉 AGGIUNTA: includi le etichette nella risposta
                "labels": labels
            }
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
