import pandas as pd

# Load the CSV file
file_path = r"D:\test\processed_gbif_split_1_pandas.csv"  # Update this path if needed
df = pd.read_csv(file_path)

# Keep all species-related columns
species_metadata_cols = ["kingdom", "phylum", "class", "order", "family", "genus", "species","Group"]

# Drop duplicates to ensure each species has unique metadata
df_species_metadata = df[species_metadata_cols].drop_duplicates()

# Create a pivot table with 'countryCode' as columns, 'species' as rows,
# and binary values (1 or 0) indicating presence of a species in a country.
df_pivot = df.pivot_table(index="species", columns="countryCode", 
                          values="scientificName", aggfunc=lambda x: 1, fill_value=0)

# Reset index to merge metadata
df_pivot_reset = df_pivot.reset_index()

# Merge the metadata with the pivot table
df_final = df_species_metadata.merge(df_pivot_reset, on="species", how="left")

# Save the final table to a CSV file
output_file_path = r"D:\test\species_presence_pivot_table.csv"  # Update the path if needed
df_final.to_csv(output_file_path, index=False)

print(f"Pivot table saved as {output_file_path}")
