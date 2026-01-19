import pandas as pd
from pandas.testing import assert_frame_equal

# -----------------------------
# Paths
# -----------------------------
csv_gpd = r"E:\FInal\N_species\polygons\species_by_biome\per_batch\species_batch_1301_species_biome.csv"
csv_arc = r"C:\Users\liu02034\Downloads\bacth_1301_SJ_Arcgis_Pro.csv"
out_diff_csv = r"C:\Users\liu02034\Downloads\species_batch_1301_differences_side_by_side.csv"

# -----------------------------
# Load (keep_default_na=True is default; good)
# -----------------------------
df_gpd = pd.read_csv(csv_gpd)
df_arc = pd.read_csv(csv_arc)

print("GeoPandas rows:", len(df_gpd))
print("ArcGIS Pro rows:", len(df_arc))

# -----------------------------
# Strip whitespace ONLY for actual strings (do not astype(str))
# -----------------------------
def strip_strings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df

df_gpd = strip_strings(df_gpd)
df_arc = strip_strings(df_arc)

# -----------------------------
# Check columns
# -----------------------------
print("\nGeoPandas columns:", list(df_gpd.columns))
print("ArcGIS Pro columns:", list(df_arc.columns))

common_cols = sorted(set(df_gpd.columns) & set(df_arc.columns))
only_in_arc = sorted(set(df_arc.columns) - set(df_gpd.columns))
only_in_gpd = sorted(set(df_gpd.columns) - set(df_arc.columns))

print("\nCommon columns:", common_cols)
print("Only in ArcGIS:", only_in_arc)
print("Only in GeoPandas:", only_in_gpd)

if not common_cols:
    raise ValueError("No common columns between the two tables; cannot compare.")

# -----------------------------
# Compare content (order-independent)
# Robust sorting: sort by string keys to avoid mixed-type issues
# -----------------------------
df1 = df_gpd[common_cols].copy()
df2 = df_arc[common_cols].copy()

# Create a stable sort key
df1["_sortkey_"] = df1.astype("string").fillna("<NA>").agg("||".join, axis=1)
df2["_sortkey_"] = df2.astype("string").fillna("<NA>").agg("||".join, axis=1)

df1 = df1.sort_values("_sortkey_").drop(columns="_sortkey_").reset_index(drop=True)
df2 = df2.sort_values("_sortkey_").drop(columns="_sortkey_").reset_index(drop=True)

# Dtype diagnostics
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

# -----------------------------
# Save differences (only if there are real value differences)
# Output = rows unique to each side, with a source label
# -----------------------------
if not value_equal:
    df1_tag = df1.copy()
    df1_tag["__source__"] = "GeoPandas"
    df2_tag = df2.copy()
    df2_tag["__source__"] = "ArcGIS_Pro"

    diff_rows = (
        pd.concat([df1_tag, df2_tag], ignore_index=True)
        .drop_duplicates(subset=common_cols, keep=False)
        .sort_values(["__source__"] + common_cols)
    )

    diff_rows.to_csv(out_diff_csv, index=False)

    print("\n⚠️ REAL value differences found.")
    print(diff_rows.head(20))
    print(f"... total differing rows: {len(diff_rows)}")
    print(f"\n📄 Differences written to:\n{out_diff_csv}")
else:
    print("\n✅ No value differences (dtype-insensitive). No diff file written.")
