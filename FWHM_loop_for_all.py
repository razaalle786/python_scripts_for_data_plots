import os
import csv
import numpy as np
import matplotlib.pyplot as plt

def calculate_fwhm(time, channel_b):
    # Find the maximum value
    max_value = max(channel_b)

    # Find the half-maximum value
    half_max = max_value / 2.0
    fwhm = time[np.where(np.array(channel_b) >= half_max)[0][0]]

    # Calculate the left and right time points where voltage equals half-max
    left_idx = np.where(np.array(channel_b) >= half_max)[0][0]
    right_idx = np.where(np.array(channel_b) >= half_max)[0][-1]
    left_time = time[left_idx]
    right_time = time[right_idx]

    # Calculate the range width for FWHM
    range_width = right_time - left_time

    # Calculate the ratio at FWHM
    count_within_range = len([value for value in channel_b if left_time <= value <= right_time])
    total_data_points = len(channel_b)
    ratio_at_fwhm = count_within_range / total_data_points

    return fwhm, range_width, ratio_at_fwhm

def process_csv_files_in_folder(csv_folder):
    # Loop through all CSV files in the folder
    for filename in os.listdir(csv_folder):
        if filename.endswith(".csv"):
            # Ignore files with special characters ('âˆž') in channel B
            csv_file_path = os.path.join(csv_folder, filename)
            special_character_flag = False

            with open(csv_file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 2:
                        if 'âˆž' in row[2]:
                            special_character_flag = True
                            break

            if special_character_flag:
                continue  # Skip files with special characters in channel B

            # Load data from the CSV file
            time = []
            channel_b = []

            with open(csv_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                next(reader)  # Skip units row
                next(reader)  # Skip empty row

                for row in reader:
                    time.append(float(row[0]))
                    channel_b.append(float(row[2]))

            # Calculate FWHM, range width, and ratio at FWHM
            max_value = max(channel_b)
            fwhm, range_width, ratio_at_fwhm = calculate_fwhm(time, channel_b)

            # Create a plot with FWHM, half-maximum line, and ratio indicated
            plt.plot(time, channel_b, label='Channel B', color = 'r')
            plt.axvline(fwhm, color='r', linestyle='--', label='FWHM')
            half_max = max_value / 2.0
            plt.axhline(half_max, color='g', linestyle='--', label='Half-Maximum')
            left_idx = np.where(np.array(channel_b) >= half_max)[0][0]
            right_idx = np.where(np.array(channel_b) >= half_max)[0][-1]
            left_time = time[left_idx]
            right_time = time[right_idx]
            plt.axvline(left_time, color='b', linestyle='--', label='Left Time')
            plt.axvline(right_time, color='b', linestyle='--', label='Right Time')
            plt.xlabel('Time')
            plt.ylabel('Channel B')
            plt.legend()
            plt.title(f'Channel B vs. Time with FWHM (Ratio at FWHM: {ratio_at_fwhm:.2f}, Range Width: {range_width:.2f})')

            # Save the plot in a folder for the specific peak type
            peak_type_folder = os.path.join(csv_folder, f'type_{determine_peak_type(max_value)}')
            os.makedirs(peak_type_folder, exist_ok=True)
            plot_filename = os.path.join(peak_type_folder, f'{filename}.png')
            plt.savefig(plot_filename)
            plt.close()

def determine_peak_type(max_value):
    if max_value >= 4.0:
        return 1
    elif max_value >= 3.0:
        return 2
    elif max_value >= 2.0:
        return 3
    elif max_value >= 1.0:
        return 4

if __name__ == '__main__':
    # Specify the folder containing the CSV files
    csv_folder = "230704_2_Co57atface_-0Vbias_1000G_12us_1.5Vthreshold_08_21_2023_002_50mm"

    # Process all CSV files in the folder
    process_csv_files_in_folder(csv_folder)
