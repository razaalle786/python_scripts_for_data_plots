import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV file into a DataFrame
csv_file_path = "230704_2_nosource_0Vbias_1000G_12us_1.5Vthreshold_230811_002.csv"
df = pd.read_csv(csv_file_path)

# Create x and y values for the scatter plot
x_values = df['Time']
y_values = df['Counts per minute']

# Plot the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(x_values, y_values, color='blue', marker='o', alpha=0.7)
plt.xlabel('Time')
plt.ylabel('Counts')
plt.title('Time vs Number of Counts')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
