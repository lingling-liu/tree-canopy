# import pandas as pd

# file_path = r"D:\01. 0007175-250127130748423\0007175-250127130748423.csv"

# # Read using tab separator
# df_sample = pd.read_csv(file_path, sep="\t", nrows=5)  # Specify sep="\t" for tab-separated files

# # Display column names correctly
# print("📋 Available Columns in CSV:")
# print(df_sample.columns.tolist())

# # Check if "kingdom" and "phylum" exist
# if "kingdom" in df_sample.columns and "phylum" in df_sample.columns:
#     print("✅ 'kingdom' and 'phylum' exist in the dataset!")
# else:
#     print("⚠️ 'kingdom' or 'phylum' is missing from the dataset!")

# import pandas as pd
# import os

# # Define file paths
# file_path = r"D:\01. 0007175-250127130748423\0007175-250127130748423.csv"
# output_dir = r"D:\gbif_splits_pandas"
# os.makedirs(output_dir, exist_ok=True)

# # Define Columns to Keep
# COLUMNS_TO_KEEP = [
#     "kingdom", "phylum", "class", "order", "family",
#     "genus", "species", "scientificName", "countryCode",
#     "decimalLatitude", "decimalLongitude"
# ]

# # Read actual column names (using tab separator)
# df_sample = pd.read_csv(file_path, sep="\t", nrows=5)

# # Standardize column names by stripping spaces
# actual_columns = df_sample.columns.str.strip()

# # Keep only columns that exist in the dataset
# COLUMNS_TO_KEEP = [col for col in COLUMNS_TO_KEEP if col in actual_columns]

# # Define chunk size (1 million rows per batch)
# chunksize = 1_000_000  

# # Initialize batch counter
# batch_number = 0  

# print(f"📊 Using Columns: {COLUMNS_TO_KEEP}")

# # Read CSV in chunks with tab separator
# for chunk in pd.read_csv(file_path, sep="\t", usecols=COLUMNS_TO_KEEP, chunksize=chunksize, low_memory=False):
#     batch_number += 1
#     output_file = os.path.join(output_dir, f"gbif_split_{batch_number}_pandas.csv")
    
#     # Save chunk to CSV
#     chunk.to_csv(output_file, index=False)
    
#     print(f"✅ Saved batch {batch_number}: {output_file} ({len(chunk)} rows)")

# print("🎉 All splits completed successfully!")


import pandas as pd
import os
import glob

# Define file paths
file_path = r"D:\01. 0007175-250127130748423\0007175-250127130748423.csv"
output_dir = r"D:\gbif_splits_pandas"
os.makedirs(output_dir, exist_ok=True)

# Define Columns to Keep
COLUMNS_TO_KEEP = [
    "kingdom", "phylum", "class", "order", "family",
    "genus", "species", "scientificName", "countryCode",
    "decimalLatitude", "decimalLongitude"
]

# Read actual column names (using tab separator)
df_sample = pd.read_csv(file_path, sep="\t", nrows=5)

# Standardize column names by stripping spaces
actual_columns = df_sample.columns.str.strip()

# Keep only columns that exist in the dataset
COLUMNS_TO_KEEP = [col for col in COLUMNS_TO_KEEP if col in actual_columns]

# Define chunk size (1 million rows per batch)
chunksize = 1_000_000  

# Find the last saved batch number
existing_files = glob.glob(os.path.join(output_dir, "gbif_split_*.csv"))
existing_batches = [int(f.split("_")[-2]) for f in existing_files if f.split("_")[-2].isdigit()]
last_batch = max(existing_batches, default=0)  # Find the last batch number
next_batch = last_batch + 1  # Start from the next batch
# print(existing_files,existing_batches,last_batch,next_batch)

print(f"📊 Resuming from batch {next_batch}...")

# Read CSV in chunks with tab separator, skipping processed batches
for batch_number, chunk in enumerate(pd.read_csv(file_path, sep="\t", usecols=COLUMNS_TO_KEEP, chunksize=chunksize, low_memory=False), start=1):
    print(batch_number)
    if batch_number < next_batch:
        continue  # Skip already processed batches

    output_file = os.path.join(output_dir, f"gbif_split_{batch_number}_pandas.csv")
    
    # Save chunk to CSV
    chunk.to_csv(output_file, index=False)
    
    print(f"✅ Saved batch {batch_number}: {output_file} ({len(chunk)} rows)")

print("🎉 All splits completed successfully!")

