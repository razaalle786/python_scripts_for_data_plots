import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy.signal import find_peaks

# Folder containing the CSV files
data_folder = "230704_2_nosource_-1Vbias_1000G_12us_1.5Vthreshold_230921_001"

# List all CSV files in the folder
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

# Initialize a list to store FWHM values
fwhm_values = []

# Loop through CSV files and calculate FWHM for the peaks
for file in csv_files:
    try:
        # Check if the filename contains special characters
        if 'âˆž' in file:
            continue  # Skip this file if it has special characters

        # Read CSV data
        data = pd.read_csv(os.path.join(data_folder, file), skiprows=[1, 2, 3])  # Skip 2nd and 3rd rows and an additional empty row

        # Extract the time series data from the first column
        time_values = data['Time']  # Adjust 'Time' to match the actual column name

        # Find peaks in the time series data
        peaks, _ = find_peaks(time_values)

        # Calculate the FWHM for each peak
        for peak_index in peaks:
            # You can implement FWHM calculation for each peak here and append the values to the fwhm_values list
            # For FWHM calculation, you'll need to determine the half-maximum level for each peak
            pass

    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Now you can work on calculating and storing FWHM values for the peaks
# You may need to adjust the FWHM calculation based on your specific data and peak characteristics
