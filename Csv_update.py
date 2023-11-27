import pandas as pd
from datetime import datetime, timedelta

# Define the start and end times
start_time_str = "12:40:00"
end_time_str = "12:40:00"
start_date = "15/08/2023"
end_date = "17/08/2023"

# Convert start and end times to datetime objects
start_datetime = datetime.strptime(f"{start_date} {start_time_str}", '%d/%m/%Y %H:%M:%S')
end_datetime = datetime.strptime(f"{end_date} {end_time_str}", '%d/%m/%Y %H:%M:%S')

# Generate time intervals by adding 30 minutes to the start time
time_intervals = []
while start_datetime < end_datetime:
    end_datetime = start_datetime + timedelta(minutes=30)
    time_interval = f"{start_datetime.strftime('%H:%M:%S')} - {end_datetime.strftime('%H:%M:%S')}"
    time_intervals.append(time_interval)
    start_datetime = end_datetime

# Create a DataFrame from the time intervals
df = pd.DataFrame({'Time': time_intervals})

# Save the data to a CSV file
csv_file_path = "230704_2_nosource_0Vbias_1000G_12us_1.5Vthreshold_230815_001.csv"
df.to_csv(csv_file_path, index=False)
