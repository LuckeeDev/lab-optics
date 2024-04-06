import numpy as np

filename = input("Enter the name of the file: ")
# Read the data from the file
x, y, yerr = np.loadtxt(filename, unpack=True)

x = x * 1e-6
# Find the maximum x value
max_y_index = np.argmax(y)
max_x = x[max_y_index]

# Filter the data based on the distance from the maximum x value
D = float(
    input("Enter the max distance from the maximum: ")
)  # Prompt the user for the value of D
mask = np.where(np.abs(x - max_x) <= D, True, False)

# Create new arrays with the filtered data
filtered_x = x[mask] * 1e6
filtered_y = y[mask]
filtered_yerr = yerr[mask]

# Write the new data to a new file
filtered_data = np.column_stack((filtered_x, filtered_y, filtered_yerr))
np.savetxt(f"{filename}_filtered", filtered_data, fmt="%.8f")
