# prosody/labeling.py

import numpy as np

LABELS = {
    "attack_soft": "Attacco morbido",
    "underline": "Sottolineatura",
    "opening": "Apertura",
    "closing": "Chiusura",
    "micro_pause": "Micro-pausa",
    "soft_tone": "Tono morbido",
    "lively_tone": "Tono vivo"
}

def detect_pitch_patterns(pitch):
    """Ritorna una lista di (index, pattern) per salite/discese."""
    patterns = []
    dp = np.diff(pitch)

    for i in range(1, len(dp)):
        if dp[i] > 0.5:   # soglia da regolare
            patterns.append((i, "opening"))
        elif dp[i] < -0.5:
            patterns.append((i, "closing"))

    return patterns

def detect_energy_patterns(energy):
    """Ritorna picchi, valli e zone vive."""
    patterns = []
    for i in range(1, len(energy)-1):
        if energy[i] > energy[i-1] and energy[i] > energy[i+1]:
            patterns.append((i, "underline"))
        elif energy[i] < energy[i-1] and energy[i] < energy[i+1]:
            patterns.append((i, "soft_tone"))

    # zona viva = variazioni rapide
    dE = np.abs(np.diff(energy))
    lively = np.where(dE > 0.3)[0]
    for i in lively:
        patterns.append((i, "lively_tone"))

    return patterns

def detect_pauses(pauses):
    """Ritorna le pause come micro-pause."""
    return [(int(p["start"] * 100), "micro_pause") for p in pauses]

def assign_labels(pitch, energy, pauses):
    """Combina tutti i pattern e restituisce etichette ordinate per tempo."""
    labels = []

    labels += detect_pitch_patterns(pitch)
    labels += detect_energy_patterns(energy)
    labels += detect_pauses(pauses)

    # ordina per tempo (index)
    labels.sort(key=lambda x: x[0])

    # converte pattern → etichetta professionale
    return [{"index": idx, "label": LABELS[tag]} for idx, tag in labels]
