import os
import csv
import numpy as np
import matplotlib.pyplot as plt

# Load the data from the CSV file
csv_file_path = '09_21_2023 17_46_34.csv'  # Replace with your file path
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

# Create a plot with FWHM, half-maximum line, and ratio indicated
plt.plot(time, channel_b, label='Channel B')
plt.axvline(fwhm, color='r', linestyle='--', label='FWHM')
plt.axhline(half_max, color='g', linestyle='--', label='Half-Maximum')
plt.axvline(left_time, color='b', linestyle='--', label='Left Time')
plt.axvline(right_time, color='b', linestyle='--', label='Right Time')
plt.xlabel('Time')
plt.ylabel('Channel B')
plt.legend()
plt.title(f'Channel B vs. Time with FWHM (Ratio at FWHM: {ratio_at_fwhm:.2f}, Range Width: {range_width:.2f})')

plt.show()
