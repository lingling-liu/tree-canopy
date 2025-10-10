import pandas as pd
import glob
import os

# Define the input directory and output file
input_dir = r"D:\test\test1"  # Update this path if needed
output_file_path = r"D:\test\species_presence_pivot_table_2files.csv"

# Find all CSV files that match the pattern
csv_files = glob.glob(os.path.join(input_dir, "processed_*.csv"))

# Initialize an empty DataFrame to store the combined pivot table
final_pivot = None

# Process each CSV file
for file in csv_files:
    # Load the CSV file
    df = pd.read_csv(file)
    
    # Create a pivot table with binary presence values (1)
    df_pivot = df.pivot_table(index="species", columns="countryCode",
                              values="scientificName", aggfunc=lambda x: 1, fill_value=0)

    # Convert to integer type to avoid float issues
    df_pivot = df_pivot.fillna(0).astype(int)

    # Merge with the existing pivot table
    if final_pivot is None:
        final_pivot = df_pivot
    else:
        # Ensure both dataframes have the same columns by aligning them
        final_pivot, df_pivot = final_pivot.align(df_pivot, fill_value=0)

        # Perform element-wise addition to merge the tables (avoiding bitwise OR)
        final_pivot = (final_pivot + df_pivot).clip(upper=1)

# Save the final merged pivot table
if final_pivot is not None:
    final_pivot.to_csv(output_file_path)
    print(f"Pivot table saved as {output_file_path}")
else:
    print("No files matched the pattern. No pivot table was created.")
