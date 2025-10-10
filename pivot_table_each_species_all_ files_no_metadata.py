import pandas as pd
import glob
import os

# Define the input directory and output file
input_dir = r"D:\gbif_splits_pandas"  # Update this path if needed
output_file_path = r"D:\species_presence_pivot_table_all_files.csv"

# Find all CSV files that match the pattern
csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

# Initialize an empty DataFrame to store the combined pivot table
final_pivot = None

# Process each CSV file
for i, file in enumerate(csv_files):
    
    print(f"Processing file {i + 1}/{len(csv_files)}: {file}")
    # Load the CSV file (only necessary columns for memory efficiency)
    df = pd.read_csv(file,low_memory=False)

    # Create a pivot table with binary presence values (1)
    df_pivot = df.pivot_table(index="species", columns="countryCode",
                              values="scientificName", aggfunc=lambda x: 1, fill_value=0)

    # Convert to uint8 to reduce memory usage
    df_pivot = df_pivot.astype("uint8")

    # Merge with the existing pivot table
    if final_pivot is None:
        final_pivot = df_pivot
    else:
        # Ensure both DataFrames have the same structure
        final_pivot, df_pivot = final_pivot.align(df_pivot, fill_value=0)

        # Ensure no NaNs appear before conversion
        final_pivot = (final_pivot.fillna(0).astype("uint8") + df_pivot.fillna(0).astype("uint8")).clip(upper=1)

    # Save intermediate results every 500 files to avoid memory overload
    if i % 500 == 0 and i > 0:
        temp_output = f"D:\\test\\temp_pivot_{i}.csv"
        final_pivot.to_csv(temp_output)
        print(f"Intermediate pivot table saved: {temp_output}")

# Save the final merged pivot table
if final_pivot is not None:
    final_pivot.to_csv(output_file_path)
    print(f"Final pivot table saved as {output_file_path}")
else:
    print("No files matched the pattern. No pivot table was created.")
