import pandas as pd
from pandas.testing import assert_frame_equal

# -----------------------------
# Paths
# -----------------------------
csv_gpd = r"E:\FInal\N_species\polygons\species_by_biome\per_batch\species_batch_1_species_biome.csv"
csv_arc = r"C:\Users\liu02034\Downloads\bacth_1_SJ_Arcgis_Pro.csv"

out_diff_csv = r"C:\Users\liu02034\Downloads\species_batch_1_differences_side_by_side.csv"

# -----------------------------
# Load
# -----------------------------
df_gpd = pd.read_csv(csv_gpd)
df_arc = pd.read_csv(csv_arc)

print("GeoPandas rows:", len(df_gpd))
print("ArcGIS Pro rows:", len(df_arc))

# -----------------------------
# Normalize text columns (strip whitespace)
# -----------------------------
for df in (df_gpd, df_arc):
    for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].astype(str).str.strip()

# -----------------------------
# Check columns
# -----------------------------
print("\nGeoPandas columns:", list(df_gpd.columns))
print("ArcGIS Pro columns:", list(df_arc.columns))

common_cols = sorted(set(df_gpd.columns) & set(df_arc.columns))
missing_in_gpd = sorted(set(df_arc.columns) - set(df_gpd.columns))
missing_in_arc = sorted(set(df_gpd.columns) - set(df_arc.columns))

print("\nCommon columns:", common_cols)
print("Only in ArcGIS:", missing_in_gpd)
print("Only in GeoPandas:", missing_in_arc)

if not common_cols:
    raise ValueError("No common columns between the two tables; cannot compare.")

# -----------------------------
# Compare content (order-independent)
# -----------------------------
df1 = df_gpd[common_cols].sort_values(common_cols).reset_index(drop=True)
df2 = df_arc[common_cols].sort_values(common_cols).reset_index(drop=True)

# Print dtype diagnostics (most common cause of equals() == False)
print("\n--- DTYPE CHECK ---")
print("df1 dtypes:\n", df1.dtypes)
print("df2 dtypes:\n", df2.dtypes)
try:
    print("\nDtype differences:\n", df1.dtypes.compare(df2.dtypes))
except Exception as e:
    print("Could not compare dtypes:", e)

# Strict equality (includes dtype)
strict_equal = df1.equals(df2)
print("\nTables identical (STRICT: values + dtypes, ignoring row order)?", strict_equal)

# Value equality ignoring dtype
try:
    assert_frame_equal(df1, df2, check_dtype=False)
    value_equal = True
except AssertionError as e:
    value_equal = False
    print("\n--- VALUE MISMATCH DETAILS (first ~500 chars) ---")
    print(str(e)[:500])

print("\nTables identical (VALUES ONLY, dtype-insensitive, ignoring row order)?", value_equal)

# -----------------------------
# If value_equal is True but strict_equal is False -> dtype-only mismatch
# -----------------------------
if value_equal and not strict_equal:
    print("\n✅ Values match, but dtypes differ (common with ArcGIS exports).")
    print("   If you want strict equality too, coerce the dtypes (example below).")

    # OPTIONAL: Coerce BIOME_NUM to a consistent integer dtype if present
    if "BIOME_NUM" in common_cols:
        df1_coerced = df1.copy()
        df2_coerced = df2.copy()

        df1_coerced["BIOME_NUM"] = pd.to_numeric(df1_coerced["BIOME_NUM"], errors="coerce").astype("Int64")
        df2_coerced["BIOME_NUM"] = pd.to_numeric(df2_coerced["BIOME_NUM"], errors="coerce").astype("Int64")

        strict_equal_after = df1_coerced.equals(df2_coerced)
        print("\nAfter coercing BIOME_NUM -> Int64, strict equality?", strict_equal_after)

# -----------------------------
# Save differences side-by-side (ONLY if there are real value differences)
# -----------------------------
if not value_equal:
    # Tag source so we can isolate which rows are unique to each
    df1_tag = df1.copy()
    df1_tag["__source__"] = "GeoPandas"
    df2_tag = df2.copy()
    df2_tag["__source__"] = "ArcGIS_Pro"

    # Rows that don't have a match in the other table (by all common_cols)
    diff_rows = pd.concat([df1_tag, df2_tag], ignore_index=True).drop_duplicates(
        subset=common_cols, keep=False
    )

    diff_gpd = diff_rows[diff_rows["__source__"] == "GeoPandas"].drop(columns="__source__")
    diff_arc = diff_rows[diff_rows["__source__"] == "ArcGIS_Pro"].drop(columns="__source__")

    # Side-by-side view: show which side each row exists in
    diff_side_by_side = diff_gpd.merge(
        diff_arc,
        on=common_cols,
        how="outer",
        indicator=True
    )

    diff_side_by_side.to_csv(out_diff_csv, index=False)

    print("\n⚠️ REAL value differences found.")
    print(diff_rows.drop(columns="__source__").head(20))
    print(f"... total differing rows: {len(diff_rows)}")
    print(f"\n📄 Side-by-side differences written to:\n{out_diff_csv}")
else:
    print("\n✅ No value differences (dtype-insensitive). No diff file written.")
