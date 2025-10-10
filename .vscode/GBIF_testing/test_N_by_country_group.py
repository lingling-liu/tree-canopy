import pandas as pd
import glob
import os

# Define folder paths
folder_path = "D:/test/"  # Path containing CSV files
output_path = "D:/test/validation_results/"  # Folder for validation outputs
os.makedirs(output_path, exist_ok=True)

# Get all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, "processed_*.csv"))

if not csv_files:
    print("❌ No CSV files found in the specified folder.")
else:
    print(f"📂 Found {len(csv_files)} files: {csv_files}")

    # Expected 10 species groups
    expected_groups = [
        "Amphibians", "Arthropods", "Birds", "Fungi", "Mammals", 
        "Reptiles", "Fish", "Plants", "Other_Animals", "Other_Kingdoms"
    ]

    # Initialize an empty DataFrame for cumulative results
    species_total = None

    # Process each file
    for file in csv_files:
        file_name = os.path.basename(file).replace(".csv", "")
        print(f"🔍 Processing file: {file}")

        # Read the CSV file
        df = pd.read_csv(file)

        # Drop missing values in `countryCode` or `Group`
        df = df.dropna(subset=["countryCode", "Group", "species"])

        # Convert countryCode to string for consistent merging
        df["countryCode"] = df["countryCode"].astype(str)

        # Count occurrences of species by country and group
        species_count = df.groupby(["countryCode", "Group"])["species"].count().reset_index()

        # Pivot so each group has its own column
        species_pivot = species_count.pivot(index="countryCode", columns="Group", values="species").fillna(0)

        # Reset index for merging
        species_pivot.reset_index(inplace=True)

        # Ensure all expected species groups exist
        for group in expected_groups:
            if group not in species_pivot.columns:
                species_pivot[group] = 0  # Add missing groups with 0 species

        # Keep only required columns and ensure correct order
        species_pivot = species_pivot[["countryCode"] + expected_groups]

        # Convert values to integers
        species_pivot[expected_groups] = species_pivot[expected_groups].astype(int)

        # Save intermediate file
        intermediate_file = os.path.join(output_path, f"{file_name}_species_count.csv")
        species_pivot.to_csv(intermediate_file, index=False)
        print(f"✅ Saved intermediate result: {intermediate_file}")

        # Merge results with cumulative data
        if species_total is None:
            species_total = species_pivot
        else:
            species_total = species_total.set_index("countryCode").add(
                species_pivot.set_index("countryCode"), fill_value=0
            ).reset_index()

    # Convert values to integers after merging
    species_total[expected_groups] = species_total[expected_groups].astype(int)

    # Save the final cumulative output
    final_output_file = os.path.join(output_path, "species_count_final.csv")
    species_total.to_csv(final_output_file, index=False)

    print(f"🎉 Processing complete. Final output saved to {final_output_file}")
