import os
import pandas as pd
import matplotlib.pyplot as plt

# Folder containing the CSV files
data_folder = "c:\Users\phra3\OneDrive - Loughborough University\Picoscope\230704_2_Co57atface_-1Vbias_1000G_12us_1.5Vthreshold_08_24_2023_001"

# List all CSV files in the folder
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

# Create a new folder for saving plots
if not os.path.exists("plots"):
    os.makedirs("plots")

# Function to create and save a scatter plot
def create_and_save_plot(file):
    # Read CSV data
    data = pd.read_csv(os.path.join(data_folder, file), skiprows=[1, 2])  # Skip 2nd and 3rd rows

    # Extract data from columns
    time = data['Time']
    channel_a = data['Channel A']
    channel_b = data['Channel B']

    # Create a new figure with two y-axes
    fig, ax1 = plt.subplots(figsize=(11.7, 8.3))  # A4 size in landscape

    # Plot Channel A data
    ax1.scatter(time, channel_a, color='blue', marker='o', label='Channel A')
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel('Channel A (mV)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a second y-axis
    ax2 = ax1.twinx()

    # Plot Channel B data on the second y-axis
    ax2.scatter(time, channel_b, color='red', marker='x', label='Channel B')
    ax2.set_ylabel('Channel B (V)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Add legend
    fig.legend(loc='upper right')

    # Save the plot as a file
    plt.savefig(os.path.join("plots", file.replace('.csv', '.png')))
    plt.close()

# Loop through CSV files and create plots
for file in csv_files:
    create_and_save_plot(file)

print("Plots generated and saved in the 'plots' folder.")

