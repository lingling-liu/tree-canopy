import pandas as pd
import glob
import os

# Define folder paths
folder_path = "D:/test/"  # Path containing CSV files
output_path = "D:/test/validation_results/"  # Folder for validation outputs
os.makedirs(output_path, exist_ok=True)

# Get the first CSV file in the folder (if available)
csv_files = glob.glob(os.path.join(folder_path, "processed_*.csv"))

if not csv_files:
    print("❌ No CSV files found in the specified folder.")
else:
    test_file = csv_files[0]  # Select the first CSV file
    print(f"📂 Processing test file: {test_file}")

    # Expected 10 species groups
    expected_groups = [
        "Amphibians", "Arthropods", "Birds", "Fungi", "Mammals", 
        "Reptiles", "Fish", "Plants", "Other_Animals", "Other_Kingdoms"
    ]

    # Read the file
    df = pd.read_csv(test_file)

    # Count occurrences of species by country and group (instead of unique species)
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

    # Save the test output
    test_output_file = os.path.join(output_path, "species_count_test.csv")
    species_pivot.to_csv(test_output_file, index=False)

    print(f"✅ Test processing complete. Output saved to {test_output_file}")
