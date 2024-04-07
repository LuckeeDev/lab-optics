import numpy as np
import os
import matplotlib.pyplot as plt

folder = input("Inserisci il percorso della cartella: ")
graph_size = float(
    input(
        "Inserisci la larghezza del grafico attorno al picco (m) (0 per lasciarlo invariato): "
    )
)

# Check if the directory exists
if not os.path.isdir(folder):
    print("Percorso non valido.")
    exit(1)


def plot():
    plt.plot(x, y, "-o", label="Dati", color="steelblue", linewidth=0.5, markersize=2)
    plt.margins(x=0)
    plt.grid(True)
    plt.legend()
    plt.xlabel("Posizione (m)")
    plt.ylabel("Intensità (V)")


for filename in os.listdir(folder):
    if filename.startswith("interferenza") and filename.endswith(".txt"):
        filepath = os.path.join(folder, filename)
        # Get dataset from file
        x, y, yerr = np.loadtxt(filepath, unpack=True)
        # Convert micrometers to meters
        x = x * 1e-6
        max_index = np.argmax(y)
        x_max = x[max_index]

        # Plot data and fit
        plot()
        plt.savefig(f"{filepath[:-4]}.pdf", bbox_inches="tight")
        plt.close()

        if graph_size != 0:
            mask = np.where(np.abs(x - x_max) < graph_size / 2)
            x = x[mask]
            y = y[mask]
            yerr = yerr[mask]

            plot()

            plt.savefig(f"{filepath[:-4]}_cut.pdf", bbox_inches="tight")
            plt.close()
