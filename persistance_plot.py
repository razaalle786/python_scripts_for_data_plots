import os
import pandas as pd
import matplotlib.pyplot as plt

# Folder containing the CSV files
data_folder = "230704_2_Co57atface_-1Vbias_1000G_12us_1.5Vthreshold_08_24_2023_001_25mm"

# List all CSV files in the folder
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

# Initialize a dictionary to store voltage and current data for each file
data_dict = {'Voltage': [], 'Current': []}

# Loop through CSV files and extract voltage and current data
for file in csv_files:
    try:
        # Read CSV data
        data = pd.read_csv(os.path.join(data_folder, file), skiprows=[1, 2])  # Skip 2nd and 3rd rows

        # Extract voltage and current data from the respective columns
        voltage = data['Voltage']
        current = data['Current']

        # Append the data to the dictionary
        data_dict['Voltage'].append(voltage)
        data_dict['Current'].append(current)

    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Create a persistence plot for voltage vs. current
plt.figure(figsize=(11.7, 8.3))  # A4 size in landscape

for i in range(len(csv_files)):
    plt.plot(data_dict['Voltage'][i], data_dict['Current'][i], label=f'File {i + 1}')

plt.xlabel('Voltage (V)')
plt.ylabel('Current (A)')
plt.title('Persistence Plot of Voltage vs. Current')
plt.legend()

# Save the persistence plot as an image file in the same folder
plt.savefig(os.path.join(data_folder, 'persistence_plot.png'))
plt.close()
