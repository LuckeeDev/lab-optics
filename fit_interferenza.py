# import libraries
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
D = float(input("Inserisci la distanza fra le fenditure (m): "))
b0 = float(input("Inserisci il rumore di fondo (V): "))  # background costante (V)
LAMBDA = float(
    input("Inserisci una stima della lunghezza d'onda (m): ")
)  # lunghezza d'onda della luce (m)
graph_size = float(
    input(
        "Inserisci la larghezza del grafico attorno al picco (m) (0 per lasciarlo invariato): "
    )
)
# x0 = float(input("Inserisci la posizione del massimo del picco di diffrazione (m): "))


# Function to be fitted
def diffrazione(x, N, b0, LAMBDA, x0, D):
    delta_x = np.abs(x - x0)
    theta = delta_x / np.sqrt(delta_x**2 + L**2)
    alpha = d / LAMBDA * theta
    beta = np.pi * D / LAMBDA * np.sin(theta)

    return b0 + N * np.sinc(alpha) ** 2 * np.cos(beta) ** 2


# Get dataset from file
x, y, yerr = np.loadtxt(filename, unpack=True)
# Convert micrometers to meters
x = x * 1e-6
# Replace zero values in yerr with a small positive number
yerr = np.where(yerr == 0, 1e-8, yerr)
max_index = np.argmax(y)
x0 = x[max_index]  # posizione del massimo del picco di diffrazione (m)
N = y[max_index]

P0 = [N, b0, LAMBDA, x0, D]
# popt, pcov = curve_fit(
#     diffrazione,  # function to be fitted (defined above)
#     x,
#     y,  # data
#     p0=P0,  # guessed parameters (used as starting values)
#     sigma=yerr,  # error on y
#     maxfev=50000,  # the more difficult is the function, the longer it takes to fit the data. If maxfev is too short, it gives a RuntimeError
# )

# errors = np.sqrt(np.diag(pcov))

# # Output fit data to a txt file
# fit_data = np.column_stack((["N", "b0", "Lambda", "x0", "D"], popt, errors))
# np.savetxt(
#     f"{filename}_fit.csv",
#     fit_data,
#     fmt="%s",
#     delimiter=",",
# )

# print("\nFIT PARAMS")
# print(f"N (V) = {popt[0]} +- {errors[0]}")
# print(f"b0 (V) = {popt[1]} +- {errors[1]}")
# print(f"Lambda (m) = {popt[2]} +- {errors[2]}")
# print(f"x0 (m) = {popt[3]} +- {errors[3]}")
# print(f"D (m) = {popt[4]} +- {errors[4]}")

# Plot data and fit
plt.margins(x=0)
plt.grid(True)

# if graph_size != 0:
#     mask = np.where(np.abs(x - popt[3]) < graph_size / 2)
#     x = x[mask]
#     y = y[mask]
#     yerr = yerr[mask]

# plt.errorbar(
#     x, y, yerr=yerr, linestyle=":", color="steelblue"
# )  # uncomment to show also errorbars
plt.plot(x, y, ".", label="Dati", color="steelblue")
# plt.plot(x, diffrazione(x, *popt), color="orange", label="Fit")

plt.legend()
plt.xlabel("Posizione (m)")
plt.ylabel("Intensità (V)")
plt.title(f"Fit interferenza ({filename})")
plt.savefig(f"./{filename}.pdf")  # --> Per salvare
# plt.show()  # --> Per visualizzare
