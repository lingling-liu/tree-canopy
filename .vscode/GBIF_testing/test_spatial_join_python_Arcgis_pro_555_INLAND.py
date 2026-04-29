import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

# -----------------------------
# Paths
# -----------------------------
csv_gpd = r"E:\FInal\N_species\polygons\species_by_inland10km\per_batch_utf8sig\species_batch_2102_species_inland10km.csv"
csv_arc = r"C:\Users\liu02034\Downloads\bacth_2102_SJ_Arcgis_Pro_inland.csv"
out_diff_csv = r"C:\Users\liu02034\Downloads\species_batch_2102_inland10km_differences_side_by_side.csv"

# -----------------------------
# Robust CSV loader for ArcGIS exports
# -----------------------------
def read_arc_csv(path: str) -> pd.DataFrame:
    attempts = [
        ("utf-8-sig", "c"),
        ("cp1252", "c"),
        ("cp1252", "python"),
        ("latin1", "c"),
        ("latin1", "python"),
    ]
    last_err = None
    for enc, eng in attempts:
        try:
            df = pd.read_csv(path, encoding=enc, engine=eng)
            print(f"✅ Loaded ArcGIS CSV with encoding={enc}, engine={eng}")
            return df
        except Exception as e:
            last_err = e
            print(f"❌ Failed ArcGIS load with encoding={enc}, engine={eng}: {type(e).__name__}: {e}")
    raise last_err

def strip_strings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df

NULL_LIKE = {"<Null>", "<NULL>", "NULL", "null", ""}

def normalize_nulls(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].apply(
                lambda x: np.nan if isinstance(x, str) and x.strip() in NULL_LIKE else x
            )
    return df

def coalesce_columns(df: pd.DataFrame, primary: str, fallback: str) -> pd.DataFrame:
    """
    If primary exists and fallback exists, fill missing primary values from fallback.
    """
    df = df.copy()
    if primary in df.columns and fallback in df.columns:
        df[primary] = df[primary].where(df[primary].notna(), df[fallback])
    return df

# -----------------------------
# Load
# -----------------------------
df_gpd = pd.read_csv(csv_gpd, encoding="utf-8-sig")
df_arc = read_arc_csv(csv_arc)

print("GeoPandas rows (raw):", len(df_gpd))
print("ArcGIS Pro rows (raw):", len(df_arc))

# Clean strings + normalize ArcGIS null markers
df_gpd = strip_strings(df_gpd)
df_arc = strip_strings(df_arc)
df_arc = normalize_nulls(df_arc)

# ✅ IMPORTANT: If ArcGIS export contains duplicate fields, coalesce them
# (very common when Spatial Join created species_1, Group_1)
df_arc = coalesce_columns(df_arc, "species", "species_1")
df_arc = coalesce_columns(df_arc, "Group", "Group_1")

# -----------------------------
# Drop ArcGIS “no-match” rows
# -----------------------------
before = len(df_arc)
for key_col in ["species", "Group", "WB_NAME"]:
    if key_col in df_arc.columns:
        pass

# Drop rows where species OR Group is missing (KEEP_ALL polygon/no-match artifacts)
if "species" in df_arc.columns and "Group" in df_arc.columns:
    df_arc = df_arc[df_arc["species"].notna() & df_arc["Group"].notna()]
else:
    raise ValueError("ArcGIS table missing expected columns 'species' and/or 'Group'.")

print(f"Dropped {before - len(df_arc)} ArcGIS rows where species OR Group is null.")
print("GeoPandas rows (post-clean):", len(df_gpd))
print("ArcGIS Pro rows (post-clean):", len(df_arc))

# -----------------------------
# Keep only the comparable columns
# -----------------------------
need_cols = ["species", "Group", "WB_NAME"]

missing_gpd = [c for c in need_cols if c not in df_gpd.columns]
missing_arc = [c for c in need_cols if c not in df_arc.columns]
if missing_gpd:
    raise ValueError(f"GeoPandas missing columns: {missing_gpd}")
if missing_arc:
    raise ValueError(f"ArcGIS missing columns: {missing_arc}")

df1 = df_gpd[need_cols].copy()
df2 = df_arc[need_cols].copy()

# Stable sort (order-independent)
df1["_sortkey_"] = df1.astype("string").fillna("<NA>").agg("||".join, axis=1)
df2["_sortkey_"] = df2.astype("string").fillna("<NA>").agg("||".join, axis=1)

df1 = df1.sort_values("_sortkey_").drop(columns="_sortkey_").reset_index(drop=True)
df2 = df2.sort_values("_sortkey_").drop(columns="_sortkey_").reset_index(drop=True)

# Compare
strict_equal = df1.equals(df2)
print("\nTables identical (STRICT)?", strict_equal)

try:
    assert_frame_equal(df1, df2, check_dtype=False)
    value_equal = True
except AssertionError as e:
    value_equal = False
    print("\n--- VALUE MISMATCH DETAILS (first ~500 chars) ---")
    print(str(e)[:500])

print("Tables identical (VALUES ONLY)?", value_equal)

# Diff output if mismatch
if not value_equal:
    df1_tag = df1.copy()
    df1_tag["__source__"] = "GeoPandas"
    df2_tag = df2.copy()
    df2_tag["__source__"] = "ArcGIS_Pro"

    diff_rows = (
        pd.concat([df1_tag, df2_tag], ignore_index=True)
        .drop_duplicates(subset=need_cols, keep=False)
        .sort_values(["__source__"] + need_cols)
    )

    diff_rows.to_csv(out_diff_csv, index=False, encoding="utf-8-sig")

    print("\n⚠️ REAL value differences found.")
    print(diff_rows.head(50))
    print(f"... total differing rows: {len(diff_rows)}")
    print(f"\n📄 Differences written to:\n{out_diff_csv}")
else:
    print("\n✅ No value differences. No diff file written.")
