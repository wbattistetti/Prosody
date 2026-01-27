def build_response(pitch, energy, rhythm, pauses, normalized, duration, sr):
    return {
        "success": True,
        "data": {
            "pitch": pitch,
            "energy": energy,
            "rhythm": rhythm,
            "pauses": pauses,
            "duration_ratio": duration / 3.0,
            "metadata": {
                "audio_duration": duration,
                "sample_rate": sr
            },
            "normalized": normalized
        }
    }
