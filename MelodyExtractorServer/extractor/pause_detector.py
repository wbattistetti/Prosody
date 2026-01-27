from pyAudioAnalysis import audioSegmentation as aS

def extract_pauses(audio, sr):
    segments = aS.silence_removal(audio, sr, 0.05, 0.05, smooth_window=0.1, weight=0.3)

    pauses = []
    for seg in segments:
        start, end = seg[0], seg[1]
        pauses.append({"start": float(start), "duration": float(end - start)})

    return pauses
