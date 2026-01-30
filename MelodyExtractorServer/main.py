@app.post("/extractor")
async def extractor(file: UploadFile = File(...)):
    try:
        # ---------------------------------------------------------
        # CHECKPOINT 1 — Lettura file
        # ---------------------------------------------------------
        audio_bytes = await file.read()
        print("CHECK 1 — audio_bytes length:", len(audio_bytes))

        audio_bytes = convert_to_linear16(audio_bytes)
        print("CHECK 1b — after convert_to_linear16:", len(audio_bytes))

        # ---------------------------------------------------------
        # CHECKPOINT 2 — Decodifica audio
        # ---------------------------------------------------------
        audio_data, sr = sf.read(io.BytesIO(audio_bytes))
        print("CHECK 2 — audio_data shape:", audio_data.shape, "sr:", sr)

        # ---------------------------------------------------------
        # CHECKPOINT 3 — Trascrizione Google
        # ---------------------------------------------------------
        words = transcribe_with_google(audio_bytes)
        print("CHECK 3 — words returned:", words)

        # ---------------------------------------------------------
        # CHECKPOINT 4 — Feature prosodiche
        # ---------------------------------------------------------
        pitch = extract_pitch(audio_data, sr)
        print("CHECK 4a — pitch len:", len(pitch))

        energy = extract_energy(audio_data, sr)
        print("CHECK 4b — energy len:", len(energy))

        rhythm = extract_rhythm(audio_data, sr)
        print("CHECK 4c — rhythm keys:", rhythm.keys())

        pauses = extract_pauses(audio_data, sr)
        print("CHECK 4d — pauses:", pauses)

        # ---------------------------------------------------------
        # CHECKPOINT 5 — Normalizzazione
        # ---------------------------------------------------------
        normalized = normalize_contours(pitch, energy)
        print("CHECK 5 — normalized types:",
              type(normalized["pitch"]),
              type(normalized["energy"]))

        # ---------------------------------------------------------
        # CHECKPOINT 6 — Labeling
        # ---------------------------------------------------------
        labels = assign_labels(
            pitch=normalized["pitch"],
            energy=normalized["energy"],
            pauses=pauses
        )
        print("CHECK 6 — labels:", labels)

        # ---------------------------------------------------------
        # CHECKPOINT 7 — Costruzione risposta JSON-safe
        # ---------------------------------------------------------
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

        print("CHECK 7 — response keys:", response["data"].keys())

        return response

    except Exception as e:
        print("🔥 EXCEPTION CAUGHT:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
