import pandas as pd

# Load the CSV file
file_path = r"D:\test\test1\processed_gbif_split_1_pandas.csv"  # Update this path if needed
df = pd.read_csv(file_path)

# Create a pivot table with 'countryCode' as columns, 'species' as rows,
# and binary values (1 or 0) indicating presence of a species in a country.
df_pivot = df.pivot_table(index="species", columns="countryCode", 
                          values="scientificName", aggfunc=lambda x: 1, fill_value=0)

# Save the pivot table to a CSV file
output_file_path = r"D:\test\species_presence_pivot_table_no_metadata.csv"  # Update the path if needed
df_pivot.to_csv(output_file_path)

print(f"Pivot table saved as {output_file_path}")
