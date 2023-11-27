import pandas as pd

def calculate_and_update_std(filename):
    # Read the CSV file
    df = pd.read_csv('generated_table.csv')

    # Calculate the standard deviation of 'Counts per minute' and 'Uncertanity'
    std_counts = df['Counts per minute'].std()
    std_uncertainty = df['Uncertanity'].std()

    # Calculate the deviations from the standard deviation
    df['Counts Deviation'] = df['Counts per minute'] - std_counts
    df['Uncertainty Deviation'] = df['Uncertanity'] - std_uncertainty

    # Update the standard deviation and deviations columns in the original DataFrame
    df.loc[0, 'Standard Deviation Counts'] = std_counts
    df.loc[0, 'Standard Deviation Uncertainty'] = std_uncertainty

    # Save the updated DataFrame back to the CSV file
    df.to_csv(filename, index=False)

# Specify the path to your CSV file
csv_filename = 'your_file.csv'

# Call the function to calculate and update standard deviation
calculate_and_update_std(csv_filename)

print("Standard deviation and deviations updated in the CSV file.")
