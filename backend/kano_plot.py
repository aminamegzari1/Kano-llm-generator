# kano_plot.py

import matplotlib.pyplot as plt
from adjustText import adjust_text

def draw_custom_kano_plot(json_data):
    cs_plus = {aspect: values["cs+"] for aspect, values in json_data.items()}
    cd_moins = {aspect: -values["cs-"] for aspect, values in json_data.items()}  # Inversé pour cohérence

    max_cs = max(cs_plus.values()) or 1
    min_cd = min(cd_moins.values()) or -1

    cs_plus_norm = {k: v / max_cs for k, v in cs_plus.items()}
    cd_moins_norm = {k: v / abs(min_cd) for k, v in cd_moins.items()}

    texts = []
    fig, ax = plt.subplots(figsize=(8, 6))

    for label, cs_value in cs_plus_norm.items():
        cd_value = cd_moins_norm.get(label, -0.5)

        if cs_value < 0.5 and cd_value < -0.5:
            color = 'red'
        elif cs_value >= 0.5 and cd_value >= -0.5:
            color = 'blue'
        elif cs_value >= 0.5 and cd_value < -0.5:
            color = 'orange'
        else:
            color = 'purple'

        ax.scatter(cs_value, cd_value, color=color)
        texts.append(ax.text(cs_value, cd_value, label, fontsize=9, ha='center', va='center', color=color))

    ax.axhline(-0.5, color='black', linestyle='dashed')
    ax.axvline(0.5, color='black', linestyle='dashed')

    ax.set_xlabel("Satisfaction CS+ (normalisé)")
    ax.set_ylabel("Dissatisfaction CD- (normalisé)")

    ax.text(0.25, 0, 'Indifferent', fontsize=10, ha='center')
    ax.text(0.75, 0, 'Attractive', fontsize=10, ha='center')
    ax.text(0.25, -0.75, 'Must-be', fontsize=10, ha='center')
    ax.text(0.75, -0.75, 'One-dimensional', fontsize=10, ha='center')

    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-1.1, 0.1)

    adjust_text(texts, ax=ax)
    ax.set_title("Diagramme de Kano (Personnalisé)")

    return fig
