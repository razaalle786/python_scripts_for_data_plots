import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Folder containing the CSV files
data_folder = "230704_2_nosource_-1Vbias_1000G_12us_900mVthreshold_08_22_2023_001"

# List all CSV files in the folder
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

# Initialize a list to store the data from Channel B
channel_b_data = []

# Initialize the time axis
time = None

# Loop through CSV files and extract Channel B data
for file in csv_files:
    try:
        # Read CSV data
        data = pd.read_csv(os.path.join(data_folder, file), skiprows=[1, 2])  # Skip 2nd and 3rd rows

        # Extract data from columns
        channel_b = data['Channel B']

        # Check if all values in Channel B are numeric
        if pd.to_numeric(channel_b, errors='coerce').notna().all():
            channel_b_data.append(channel_b.values)
            # If time is not initialized, use the time axis from this file
            if time is None:
                time = data['Time'].values
    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Calculate the average of Channel B data if there is valid data
if channel_b_data and time is not None:
    # Create a 2D array from the extracted data
    channel_b_array = np.vstack(channel_b_data)

    # Calculate the average along axis 0 (average of corresponding rows)
    average_channel_b = np.nanmean(channel_b_array, axis=0)
    
    # Plot the average values using the time axis from one of the files
    plt.figure(figsize=(11.7, 8.3))  # A4 size in landscape
    plt.scatter(time, average_channel_b, color='blue', marker='*', label='Average Channel B')
    plt.xlabel('Time (ms)')
    plt.ylabel('Channel B (V)')
    plt.ylim(-2, 5)
    plt.xlim(-5, 5)  # Set the x-axis limits from -5 ms to 5 ms
    plt.legend(loc='upper right')
    plt.title('Average Channel B Value Across CSV Files')

    # Save the plot as a file in the same folder
    plt.savefig(os.path.join(data_folder, 'average_ChannelB.png'))
    plt.close()
else:
    print("No valid numeric values in Channel B across all files or no common time axis.")
