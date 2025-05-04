# kano_fusion.py

import json
import numpy as np

def classify_kano(cs_plus, cs_minus):
    """
    Classe chaque aspect selon les scores cs+ et cs-
    Retourne un dictionnaire : {"aspect": {cs+, cs-, category}}
    """
    result = {}
    max_cs = max(cs_plus.values()) or 1
    max_cd = max(abs(v) for v in cs_minus.values()) or 1

    for aspect in cs_plus:
        cs = cs_plus[aspect] / max_cs
        cd = -cs_minus.get(aspect, 0.0) / max_cd  # inversé car - = insatisfaction

        # Catégorisation Kano
        if cs >= 0.5 and cd >= -0.5:
            category = "Attractive"
        elif cs < 0.5 and cd < -0.5:
            category = "Must-be"
        elif cs >= 0.5 and cd < -0.5:
            category = "One-dimensional"
        else:
            category = "Indifferent"

        result[aspect] = {
            "cs+": round(cs, 2),
            "cs-": round(-cd, 2),  # Retourne à l’échelle négative pour le plot
            "category": category
        }

    return result


# Exemple d'utilisation (remplace ceci avec ton JSON Gemini ou NLP)
if __name__ == "__main__":
    with open("kano_scores.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    cs_plus = {k: v["cs+"] for k, v in data.items()}
    cs_minus = {k: v["cs-"] for k, v in data.items()}

    kano_fusion = classify_kano(cs_plus, cs_minus)
    print(json.dumps(kano_fusion, indent=2, ensure_ascii=False))
