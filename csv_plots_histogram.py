import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Folder containing the CSV files
data_folder = "230704_2_Co57atface_-1Vbias_1000G_12us_1.5Vthreshold_08_24_2023_001_25mm"

# List all CSV files in the folder
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

# Initialize a list to store the maximum positive voltage values
max_voltage_values = []

# Loop through CSV files and extract the maximum positive voltage values
for file in csv_files:
    try:
        # Read CSV data
        data = pd.read_csv(os.path.join(data_folder, file), skiprows=[1, 2])  # Skip 2nd and 3rd rows

        # Extract data from the 'Channel B' column
        channel_b = data['Channel B']

        # Convert channel_b to numeric, ignoring non-numeric values
        channel_b_numeric = pd.to_numeric(channel_b, errors='coerce')

        # Filter out non-numeric values
        channel_b_numeric = channel_b_numeric.dropna()

        # Find the maximum positive value, round it, and add to the list
        max_positive_value = channel_b_numeric[channel_b_numeric > 0].max()
        if not np.isnan(max_positive_value):
            max_voltage_values.append(round(max_positive_value))

    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Create a histogram of the rounded maximum positive voltage values
plt.figure(figsize=(11.7, 8.3))  # A4 size in landscape
plt.hist(max_voltage_values, bins=np.arange(0, 6, 0.5), color='purple', edgecolor='black')
plt.xlabel('Maximum Positive Voltage (V)')
plt.ylabel('Number of Occurrences')

# Construct a label string with date and additional information
additional_info = "Additional Information: Your Text Here"
placeholder_date = '2023-08-24'
label_text = f'Date: 24-8-2023\n Co-57 att 25 mm'

# Set the title and label with the constructed text
plt.title('Histogram of Maximum Positive Voltage Values\n' + label_text)

# Adjust the position of the label
plt.annotate(label_text, xy=(0.5, -0.15), xycoords='axes fraction', fontsize=10, ha='center')

plt.xticks(range(6))
plt.xlim(0, 5)

# Identify non-numeric values and plot them above 5 V in red
non_numeric_values = [v for v in max_voltage_values if v > 5]
if non_numeric_values:
    plt.hist(non_numeric_values, bins=np.arange(6, max(non_numeric_values) + 1, 1), color='red', edgecolor='black', alpha=0.5)

# Save the histogram as a file in the same folder
plt.savefig(os.path.join(data_folder, 'max_voltage_histogram.png'))
plt.close()