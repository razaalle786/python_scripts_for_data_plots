import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Folder containing the CSV files
data_folder = "230704_2_Co57atface_-1Vbias_1000G_12us_1.5Vthreshold_08_24_2023_001_25mm"

# List all CSV files in the folder
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

# Initialize a list to store the maximum positive voltage values
max_voltage_values = []

# Define the start and end times for the 18-hour period
start_time = datetime(2023, 8, 24, 15, 50)  # Start time
end_time = start_time + timedelta(hours=18)  # End time is 18 hours later

# Loop through CSV files and extract the maximum positive voltage values within the 18-hour period
for file in csv_files:
    try:
        # Extract the timestamp from the filename (assuming the filename format is consistent)
        filename_parts = file.split(".")
        if len(filename_parts) == 2:
            timestamp_str = filename_parts[0]
        else:
            continue  # Skip this file if the filename format is unexpected

        # Modify the format to match MM_DD_YYYY HH_MM_SS
        timestamp = datetime.strptime(timestamp_str, "%m_%d_%Y %H_%M_%S")

        # Check if the timestamp is within the 18-hour period
        if start_time <= timestamp <= end_time:
            # Read CSV data
            data = pd.read_csv(os.path.join(data_folder, file), skiprows=[1, 2])  # Skip 2nd and 3rd rows

            # Extract data from the 'Channel B' column
            channel_b = data['Channel B']

            # Convert channel_b to numeric, ignoring non-numeric values
            channel_b_numeric = pd.to_numeric(channel_b, errors='coerce')

            # Filter out non-numeric values
            channel_b_numeric = channel_b_numeric.dropna()
            channel_b_numeric = channel_b_numeric.abs().dropna()

            # Find the maximum positive value and add to the list
            max_positive_value = channel_b_numeric[channel_b_numeric > 0].max()
            if not np.isnan(max_positive_value):
                max_voltage_values.append(max_positive_value)

    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Create a histogram of the maximum positive voltage values with 0.2 V intervals
plt.figure(figsize=(11.7, 8.3))  # A4 size in landscape
bins = np.arange(0, 5, 0.2)  # Adjust the bins to have 0.2 V intervals
plt.hist(max_voltage_values, bins=bins, color='r', edgecolor='black')
plt.xlabel('Maximum Positive Voltage (V)', fontsize= 20)
plt.ylabel('Number of Occurrences', fontsize= 20)

# Construct a label string with date and additional information
additional_info = "230704_2_Co57atface_-1Vbias_1000G_12us_1.5Vthreshold_08_24_2023_001_25mm"
label_text = f'Date: {start_time.strftime("%d-%m-%Y")}\n Co57-1 V for 18 hours'

# Set the title and label with the constructed text
plt.title('Histogram of Maximum Positive Voltage Values for Amp\n' + label_text, fontsize =20 )

# Adjust the position of the label
#plt.annotate(label_text, xy=(0.5, -0.15), xycoords='axes fraction', fontsize=20, ha='center')

plt.xticks(np.arange(0, 5, 1))  # Adjust the x-axis ticks
plt.xlim(0, 5)
plt.xticks(fontsize=20)  # Increase font size for x-axis tick labels
plt.yticks(fontsize=20)
# Identify non-numeric values and plot them above 5 V in red
non_numeric_values = [v for v in max_voltage_values if v > 20.0]
if non_numeric_values:
    plt.hist(non_numeric_values, bins=np.arange(10, max(non_numeric_values) + 1, 1), color='r', edgecolor='black', alpha=0.5)

# Save the histogram as a file in the same folder
plt.savefig(os.path.join(data_folder, 'Co57 -1Vbias230824_histogram.png'))
plt.close()