import matplotlib.pyplot as plt
import numpy as np

def plot_startup_radar(startup_row):

    categories = ["Product", "Team", "Traction", "Innovation"]

    values = [
        startup_row["product_score"],
        startup_row["team_score"],
        startup_row["traction_score"],
        startup_row["innovation_score"]
    ]

    values += values[:1]

    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    ax.set_yticklabels([])
    ax.set_title(f"{startup_row['startup_name']} Radar Chart")

    return fig