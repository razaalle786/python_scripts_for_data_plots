import os
import csv

csv_folder = "230704_2_Co57atface_-0Vbias_1000G_12us_1.5Vthreshold_08_21_2023_002_50mm"

type_1_count = 0
type_2_count = 0
type_3_count = 0
type_4_count = 0
type_5_count = 0

for filename in os.listdir(csv_folder):
    if filename.endswith(".csv"):
        csv_file_path = os.path.join(csv_folder, filename)
        max_voltage = -float('inf')
        special_character_flag = False

        with open(csv_file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            next(reader)  # Skip units row
            next(reader)  # Skip empty row

            for row in reader:
                try:
                    channel_b_value = float(row[2])

                    if channel_b_value > max_voltage:
                        max_voltage = channel_b_value
                except ValueError:
                    special_character_flag = True
                except IndexError:
                    special_character_flag = True

        if max_voltage >= 4.0:
            type_1_count += 1
        elif max_voltage >= 3.0:
            type_2_count += 1
        elif max_voltage >= 2.0:
            type_3_count += 1
        elif max_voltage >= 1.0:
            type_4_count += 1

        if special_character_flag:
            type_5_count += 1
type_1_count = type_1_count - type_5_count
total_counts = type_1_count + type_2_count +type_3_count+type_4_count +type_5_count
print(f"Type 1 Count: {type_1_count}")
print(f"Type 2 Count: {type_2_count}")
print(f"Type 3 Count: {type_3_count}")
print(f"Type 4 Count: {type_4_count}")
print(f"Type 5 (Special Character) Count: {type_5_count}")
print(f"Total Count:{total_counts}")
