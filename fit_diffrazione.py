import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

# Initial parameters
filename = input("Inserisci il nome del file: ")
L = float(
    input("Inserisci la distanza fra la fenditura e lo schermo (m): ")
)  # distanza fenditura - schermo (m)
d = float(
    input("Inserisci la larghezza della fenditura (m): ")
)  # larghezza della fenditura (m)
b0 = float(input("Inserisci il rumore di fondo (V): "))  # background costante (V)
LAMBDA = float(
    input("Inserisci una stima della lunghezza d'onda (m): ")
)  # lunghezza d'onda della luce (m)
graph_size = float(
    input(
        "Inserisci la larghezza del grafico attorno al picco (m) (0 per lasciarlo invariato): "
    )
)


# Function to be fitted
def diffrazione(x, N, b0, LAMBDA, x_max):
    delta_x = x_max - x
    y = d / LAMBDA * delta_x / np.sqrt(delta_x**2 + L**2)

    return b0 + N * np.sinc(y) ** 2


# Get dataset from file
x, y, yerr = np.loadtxt(filename, unpack=True)
# Convert micrometers to meters
x = x * 1e-6
# Replace zero values in yerr with a small positive number
yerr = np.where(yerr == 0, 1e-8, yerr)
max_index = np.argmax(y)
x_max = x[max_index]
N = y[max_index]

P0 = [N, b0, LAMBDA, x_max]
popt, pcov = curve_fit(
    diffrazione,
    x,
    y,
    p0=P0,
    sigma=yerr,
    maxfev=50000,
)

errors = np.sqrt(np.diag(pcov))

# Output fit data to a txt file
fit_data = np.column_stack((["N", "b0", "Lambda", "x_max"], popt, errors))
np.savetxt(
    f"{filename[:-4]}_fit.csv",
    fit_data,
    fmt="%s",
    delimiter=",",
)

print("\nFIT PARAMS")
print(f"N (V) = {popt[0]} +- {errors[0]}")
print(f"b0 (V) = {popt[1]} +- {errors[1]}")
print(f"Lambda (m) = {popt[2]} +- {errors[2]}")
print(f"x_max (m) = {popt[3]} +- {errors[3]}")

# Plot data and fit
plt.margins(x=0)
plt.grid(True)

if graph_size != 0:
    mask = np.where(np.abs(x - popt[3]) < graph_size / 2)
    x = x[mask]
    y = y[mask]
    yerr = yerr[mask]

plt.plot(x, y, ".", label="Dati", color="steelblue")
# plt.errorbar(x, y, yerr=yerr, fmt="none", label="Dati", color="steelblue")
plt.plot(x, diffrazione(x, *popt), color="orange", label="Fit")

plt.legend()
plt.xlabel("Posizione (m)")
plt.ylabel("Intensità (V)")
plt.savefig(f"{filename[:-4]}.pdf")
