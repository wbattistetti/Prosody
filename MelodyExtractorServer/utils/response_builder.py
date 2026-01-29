def build_response(pitch, energy, rhythm, pauses, normalized, duration, sr):
    # Helper per convertire qualsiasi numpy array in lista
    def safe(x):
        if hasattr(x, "tolist"):
            return x.tolist()
        return x

    return {
        "success": True,
        "data": {
            "pitch": safe(pitch),
            "energy": safe(energy),
            "rhythm": safe(rhythm),
            "pauses": safe(pauses),
            "duration_ratio": float(duration) / 3.0,
            "metadata": {
                "audio_duration": float(duration),
                "sample_rate": int(sr)
            },
            "normalized": safe(normalized)
        }
    }
