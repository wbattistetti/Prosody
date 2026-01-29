from pyAudioAnalysis import audioSegmentation as aS

def extract_pauses(audio, sr):
    # Segmentazione basata sul silenzio
    segments = aS.silence_removal(
        audio,
        sr,
        0.05,  # soglia bassa
        0.05,  # soglia alta
        smooth_window=0.1,
        weight=0.3
    )

    pauses = []
    for seg in segments:
        start, end = float(seg[0]), float(seg[1])
        pauses.append({
            "start": start,
            "duration": float(end - start)
        })

    # Debug per verificare cosa torna davvero
    print("DEBUG extract_pauses:", pauses)

    return pauses
