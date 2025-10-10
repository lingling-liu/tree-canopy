import pandas as pd
import glob
import os

# Define input folder containing multiple CSV files
input_folder = r"D:\test\test1"  # Update with your folder path
#output_file_path = os.path.join(input_folder, "species_presence_pivot_table.csv")
output_file_path = "D:\testspecies_presence_pivot_table.csv"

# Find all processed CSV files
csv_files = glob.glob(os.path.join(input_folder, "processed_*.csv"))

# Define species-related metadata columns
species_metadata_cols = ["kingdom", "phylum", "class", "order", "family", "genus", "species", "Group"]

# Initialize empty DataFrame for combined results
df_combined_metadata = pd.DataFrame(columns=species_metadata_cols)
df_combined_pivot = pd.DataFrame()

# Process each file and merge the results
for file in csv_files:
    print(f"Processing {file}...")

    # Load data
    df = pd.read_csv(file, low_memory=False)

    # Extract species metadata and remove duplicates
    df_species_metadata = df[species_metadata_cols].drop_duplicates()

    # Create pivot table: 'species' as index, 'countryCode' as columns, presence (1 or 0)
    df_pivot = df.pivot_table(index="species", columns="countryCode", 
                              values="scientificName", aggfunc=lambda x: 1, fill_value=0)

    # Merge species metadata
    df_species_metadata = df_species_metadata.merge(df_pivot.reset_index(), on="species", how="left")

    # Combine metadata from all files (drop duplicates)
    df_combined_metadata = pd.concat([df_combined_metadata, df_species_metadata], ignore_index=True).drop_duplicates()

    # Merge species presence (keep `1` where a species is present in a country)
    if df_combined_pivot.empty:
        df_combined_pivot = df_pivot
    else:
        df_combined_pivot = df_combined_pivot.combine_first(df_pivot)  # Retains existing `1`s

# Reset index before merging with metadata
df_combined_pivot_reset = df_combined_pivot.reset_index()

# Merge final metadata with the species presence pivot table
df_final = df_combined_metadata.merge(df_combined_pivot_reset, on="species", how="left")

# Save the final combined table to a CSV file
df_final.to_csv(output_file_path, index=False)

print(f"\nFinal combined pivot table saved as: {output_file_path}")
