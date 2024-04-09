import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 24, "font.family": "Calibri"})

graph1 = "interferenza_4.txt"
graph2 = "interferenza_3.txt"
graph3 = "interferenza_5.txt"
graph4 = "interferenza_6.txt"

# Load data from files
data1 = np.loadtxt(graph1, unpack=True)
data2 = np.loadtxt(graph2, unpack=True)
data3 = np.loadtxt(graph3, unpack=True)
data4 = np.loadtxt(graph4, unpack=True)

data = [data1, data2, data3, data4]
masks = []

for i in range(len(data)):
    x, y, y_err = data[i]
    x = x * 1e-6
    max_index = np.argmax(y)
    x_max = x[max_index]

    mask = np.where(np.abs(x - x_max) <= 0.005)
    masks.append(mask)

# Create subplots
fig, axs = plt.subplots(2, 2)
fig.subplots_adjust(left=0.06, bottom=0.08, right=0.94, top=0.94)

# Plot data on subplots
axs[0, 0].plot(
    data1[0][masks[0]] * 1e-6,
    data1[1][masks[0]],
    "-o",
    color="steelblue",
    markersize=2,
    linewidth=0.5,
    label="Dati",
)
axs[0, 0].set_title("Fenditura 1")
axs[0, 0].set_ylabel("Intensità (V)")

axs[0, 1].plot(
    data2[0][masks[1]] * 1e-6,
    data2[1][masks[1]],
    "-o",
    color="steelblue",
    markersize=2,
    linewidth=0.5,
    label="Dati",
)
axs[0, 1].set_title("Fenditura 2")

axs[1, 0].plot(
    data3[0][masks[2]] * 1e-6,
    data3[1][masks[2]],
    "-o",
    color="steelblue",
    markersize=2,
    linewidth=0.5,
    label="Dati",
)
axs[1, 0].set_title("Fenditura 3")
axs[1, 0].set_xlabel("Posizione (m)")
axs[1, 0].set_ylabel("Intensità (V)")

axs[1, 1].plot(
    data4[0][masks[3]] * 1e-6,
    data4[1][masks[3]],
    "-o",
    color="steelblue",
    markersize=2,
    linewidth=0.5,
    label="Dati",
)
axs[1, 1].set_title("Fenditura 4")
axs[1, 1].set_xlabel("Posizione (m)")

for ax in axs.flat:
    ax.margins(x=0)
    ax.grid(True)
    ax.legend()

# Show the plot
plt.show()
