import os
import csv
import shutil

# Step 1: Create a subfolder
subfolder_name = "special_character230704_2_Co57atface_-0Vbias_1000G_12us_1.5Vthreshold_08_21_2023_002_50mm"
os.makedirs(subfolder_name, exist_ok=True)

# Step 2: Loop through CSV files
csv_folder = "230704_2_Co57atface_-0Vbias_1000G_12us_1.5Vthreshold_08_21_2023_002_50mm"  # Replace with the path to your CSV files
special_character_count = 0

for filename in os.listdir(csv_folder):
    if filename.endswith(".csv"):
        csv_file_path = os.path.join(csv_folder, filename)

        # Step 3: Check for special characters in Channel B
        with open(csv_file_path, "r") as file:
            reader = csv.reader(file)

            # Skip the first three rows
            for _ in range(3):
                next(reader)

            for row in reader:
                # Modify this portion to check if the value in Channel B is not a valid float
                channel_b_value = row[2]  # Change [2] to the appropriate index for Channel B
                try:
                    # Attempt to convert the value to a float
                    float_value = float(channel_b_value)
                except ValueError:
                    # If a ValueError occurs, it's not a valid float
                    special_character_count += 1
                    # Step 4: Copy the file to the subfolder
                    shutil.copy(csv_file_path, os.path.join(subfolder_name, filename))
                    break  # No need to continue checking the same file

print(f"Files with special characters found: {special_character_count}")
