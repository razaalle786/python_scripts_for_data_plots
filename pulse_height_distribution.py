import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# List of folders containing the CSV files along with source and date information
data_folders_info = [
    {"folder": "230704_2_nosource_-1Vbias_1000G_12us_1.5Vthreshold_230921_001", "source": "no_source", "date": "2023-09-21", "color": "b"},
    {"folder": "230704_2_Co57atface_-1Vbias_1000G_12us_1.5Vthreshold_08_24_2023_001_25mm", "source": "co57", "date": "2023-08-24", "color": "r"},
    {"folder": "230704_2_Co57atface_-1Vbias_1000G_12us_1.5Vthreshold_08_23_2023_001_50mm", "source": "co57", "date": "2023-08-23", "color": "g"},
    {"folder": "230704_2_nosource_-1Vbias_1000G_12us_900mVthreshold_08_22_2023_001", "source": "no_source", "date": "2023-08-22", "color": "purple"}
]

# Initialize a list to store the maximum positive voltage values for each folder
max_voltage_values = []

# Loop through the folders
for folder_info in data_folders_info:
    folder = folder_info["folder"]

    # Initialize a list to store the maximum positive voltage values for the current folder
    max_voltage_values_folder = []

    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(folder) if f.endswith(".csv")]

    # Loop through CSV files in the current folder
    for file in csv_files:
        try:
            # Read CSV data
            data = pd.read_csv(os.path.join(folder, file), skiprows=[1, 2])  # Skip 2nd and 3rd rows

            # Extract data from the 'Channel B' column
            channel_b = data['Channel B']

            # Convert channel_b to numeric, ignoring non-numeric values
            channel_b_numeric = pd.to_numeric(channel_b, errors='coerce')

            # Filter out non-numeric values
            channel_b_numeric = channel_b_numeric.dropna()

            # Find the maximum positive value and add to the list
            max_positive_value = channel_b_numeric[channel_b_numeric > 0].max()
            if not pd.isna(max_positive_value):
                max_voltage_values_folder.append(max_positive_value)

        except Exception as e:
            print(f"Error processing file {file} in folder {folder}: {e}")

    max_voltage_values.extend(max_voltage_values_folder)

# Create a probability density plot (kernel density plot)
plt.figure(figsize=(11.7, 8.3))  # A4 size in landscape

# Loop through folders to customize plot colors and legend labels
for folder_info in data_folders_info:
    color = folder_info["color"]
    label = f"{folder_info['source']}, {folder_info['date']}"
    sns.kdeplot(max_voltage_values, fill=False, color=color, label=label, lw=2)  # Customize line width


plt.xlabel('Maximum Positive Voltage (V)', fontsize=20)
plt.ylabel('Probability Density', fontsize=20)
plt.xticks(fontsize=20)  # Increase font size for x-axis tick labels
plt.yticks(fontsize=20)  # Increase font size for y-axis tick labels

# Increase font size for title
plt.title('Pulse Height Distribution for Different Data Sources at -1 V bias', fontsize=20)

# Customize legend font size and marker size
plt.legend(fontsize=20, markerscale=8)

# Save the pulse height distribution plot
plt.savefig('pulse_height_distribution at -1 V.png')