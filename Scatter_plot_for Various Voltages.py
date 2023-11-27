import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# List of folders containing the CSV files along with source and date information
data_folders_info = [
    {"folder": "230704_2_Co57_25mm_0Vbias_1000G_12us_1.5Vthreshold_230920_001", "source": "Co57", "date": "2023-09-20", "color": "r"},
    {"folder": "230704_2_nosource_0Vbias_1000G_12us_1.5Vthreshold_230919_001", "source": "no_source", "date": "2023-09-19", "color": "b"},
    {"folder": "230704_2_Co57atface_-0Vbias_1000G_12us_1.5Vthreshold_08_21_2023_002_50mm", "source": "Co57", "date": "2023-08-21", "color": "purple"},
]

# Initialize a dictionary to store data for each folder
folder_data = {}

# Loop through the folders
for folder_info in data_folders_info:
    folder = folder_info["folder"]
    source = folder_info["source"]

    # Initialize lists to store data for scatter plot
    max_voltage_values = []
    num_counts_values = []

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
                max_voltage_values.append(max_positive_value)

            # Add the number of counts to the list
            num_counts_values.append(len(channel_b_numeric))

        except Exception as e:
            print(f"Error processing file {file} in folder {folder}: {e}")

    # Store data for the current folder in the dictionary
    folder_data[source] = {"max_voltage": max_voltage_values, "num_counts": num_counts_values}

# Create a scatter plot
plt.figure(figsize=(11.7, 8.3))  # A4 size in landscape

# Plot scatter plots for each folder
for source, data in folder_data.items():
    plt.scatter(data["max_voltage"], data["num_counts"], label=source)

plt.xlabel('Maximum Positive Voltage (V)', fontsize=20)
plt.ylabel('Number of Counts', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('Scatter Plot of Maximum Voltage vs. Number of Counts for Different Folders', fontsize=20)
plt.legend(fontsize=15)

# Save the scatter plot
plt.savefig('scatter_plot_max_voltage_vs_counts_folders.png')

# Show the plot
plt.show()
