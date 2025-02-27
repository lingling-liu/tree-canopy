import duckdb
import os

# Detect number of CPU cores
num_threads = os.cpu_count()

# Define file path
file_path = r"D:\01. 0007175-250127130748423\0007175-250127130748423.csv"
output_dir = r"D:\gbif_splits_test"  # Directory to store split files
os.makedirs(output_dir, exist_ok=True)  # Create directory if not exists

# Enable multi-threading
duckdb.query(f"PRAGMA threads={num_threads};")  # Use all available CPU cores

# Columns to keep (Make sure these columns exist in your CSV)
COLUMNS_TO_KEEP = [
    "kingdom", "phylum", "class", "order", "family",
    "genus", "species", "scientificName", "countryCode", 
    "decimalLatitude", "decimalLongitude"
]

# Convert column names into safe SQL format
formatted_columns = ", ".join(f'"{col}"' for col in COLUMNS_TO_KEEP)  # Ensures safe quoting

# Correct total rows (Ensure it's an integer)
total_rows = 3_078_920_317  # Use underscore format or integer

# Compute number of files (Ensuring integer)
num_files = int((total_rows // 1_000_000) + (1 if total_rows % 1_000_000 else 0))

print(f"📊 Total rows in dataset: {total_rows} (Splitting into {num_files} files of 1M each)")

# Split into 1M-row files
for i in range(num_files):
    offset = i * 1_000_000  # Offset for each file

    print(f"🔄 Processing batch {i+1}/{num_files} (Offset: {offset})")

    # SQL Query to fetch 1M rows at a time
    query = f"""
        SELECT {formatted_columns}
        FROM read_csv_auto('{file_path}', types={{'eventDate': 'VARCHAR'}})
        LIMIT 1000000 OFFSET {offset}  -- Process in batches of 1 million rows
    """

    # Run the query
    df = duckdb.query(query).df()

    # Save to CSV
    output_file = os.path.join(output_dir, f"gbif_split_{i+1}.csv")
    df.to_csv(output_file, index=False)
    print(f"✅ Saved: {output_file} ({len(df)} rows)")

print("🎉 All splits completed successfully!")
