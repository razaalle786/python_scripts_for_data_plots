import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Folder containing the CSV files
data_folder = "230704_2_Co57_25mm_0Vbias_1000G_12us_1.5Vthreshold_230920_001"

# List all CSV files in the folder
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

# Initialize variables to store the running sum and count for Channel B
running_sum_channel_b = None
count = 0

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
            # If time is not initialized, use the time axis from this file
            if time is None:
                time = data['Time'].values

            # Convert channel_b to a NumPy array
            channel_b_values = channel_b.values

            # Update the running sum and count
            if running_sum_channel_b is None:
                running_sum_channel_b = channel_b_values
            else:
                running_sum_channel_b += channel_b_values

            count += 1
    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Calculate the average of Channel B data if there is valid data
if count > 0 and time is not None:
    # Calculate the average as the running sum divided by the count
    average_channel_b = running_sum_channel_b / count
    
    # Plot the average values using the time axis from one of the files
    plt.figure(figsize=(11.7, 8.3))  # A4 size in landscape
    plt.scatter(time, average_channel_b, color='red', marker='o', label='No source (0V) 0821023')
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
