def build_response(pitch, energy, rhythm, pauses, normalized, duration, sr):

    def safe(x):
        # numpy scalar → float/int
        if hasattr(x, "item"):
            return x.item()

        # numpy array → list
        if hasattr(x, "tolist"):
            return x.tolist()

        # bytes → stringa base64
        if isinstance(x, (bytes, bytearray)):
            return x.decode("latin1")  # evita crash UTF-8

        # lista → safe() ricorsivo
        if isinstance(x, list):
            return [safe(i) for i in x]

        # dizionario → safe() ricorsivo
        if isinstance(x, dict):
            return {k: safe(v) for k, v in x.items()}

        # tutto il resto è già JSON-safe
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
