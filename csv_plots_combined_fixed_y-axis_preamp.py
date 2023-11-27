import os
import pandas as pd
import matplotlib.pyplot as plt

# Folder containing the CSV files
data_folder = "230704_2_nosource_-1Vbias_1000G_12us_1.5Vthreshold_230921_001"

# Create a folder to save the images with "preAmp" added to their names
image_folder = "preAmp_images_noSource_09_22_23_-1V"
os.makedirs(image_folder, exist_ok=True)

# List all CSV files in the folder
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

# Function to create and save a scatter plot for Channel B
def create_and_save_plot(file):
    # Read CSV data
    data = pd.read_csv(os.path.join(data_folder, file), skiprows=[1, 2])  # Skip 2nd and 3rd rows

    # Extract data from columns
    time = data['Time']
    channel_a = data['Channel A']

    # Create the scatter plot for Channel A
    plt.figure(figsize=(11.7, 8.3))  # A4 size in landscape
    plt.scatter(time, channel_a, color='blue', marker='*', label='Channel A')
    plt.xlabel('Time (ms)')
    plt.ylabel('Channel A (mV)')
    plt.ylim(-20, 5)  # Set the Y-axis limits from -5 to 5
    plt.legend(loc='upper right')
    plt.title(file)  # Use the file name as the plot title

    # Save the plot as a file in the new folder with "preAmp" added to the name
    image_name = file.replace('.csv', '_preAmp_ChannelA.png')
    plt.savefig(os.path.join(image_folder, image_name))
    plt.close()

# Loop through CSV files and create plots for Channel A
for file in csv_files:
    create_and_save_plot(file)

print("Plots for Channel A generated and saved in the 'preAmp_images' folder.")
