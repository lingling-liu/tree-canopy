import os
import pandas as pd
import unicodedata

# ============================================================
# USER PATHS
# ============================================================
TABLE_B = r"C:\Users\liu02034\Downloads\bacth_1_WB_SJ.csv"  # ArcGIS output
TABLE_A = r"E:\FInal\N_species\polygons\species_by_country\species_batch_1_intersection_WB_countries.csv"

OUT_COMPARE = r"E:\FInal\N_species\polygons\species_by_country\compare_country_group_counts_batch_1_FINAL.csv"

REQUIRED_COLS = {"WB_NAME", "Group", "species"}
NULL_LIKE = {"", "nan", "none", "null", "<null>", "<Null>", "NA", "N/A"}

# ============================================================
# MANUAL NAME FIXES (add more as you find them)
#   Left side = bad/ArcGIS-corrupted
#   Right side = correct name used by WB table
# ============================================================
NAME_MAP = {
    'Cura‡ao (Neth.)': 'Curaçao (Neth.)',
    'C"te d\'Ivoire': "Côte d'Ivoire",
    "C“te d'Ivoire": "Côte d'Ivoire",          # just in case another variant appears
    "Cote d'Ivoire": "Côte d'Ivoire",          # optional
    'S?o Tom‚ and Pr¡ncipe': 'São Tomé and Príncipe',
    'Saint-Barth‚lemy (Fr.)': 'Saint-Barthélemy (Fr.)',
}

# ============================================================
# READERS
# ============================================================
def read_csv_safely(path: str) -> pd.DataFrame:
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path, encoding="latin1")

# ============================================================
# TEXT NORMALIZATION
# ============================================================
def normalize_text(x):
    if pd.isna(x):
        return None

    s = str(x).replace("\ufeff", "").strip()
    if s.lower() in {t.lower() for t in NULL_LIKE}:
        return None

    # unicode normalize
    s = unicodedata.normalize("NFKC", s)

    # normalize punctuation variations
    s = (
        s.replace("’", "'")
         .replace("‘", "'")
         .replace("“", '"')
         .replace("”", '"')
         .replace("–", "-")
         .replace("—", "-")
         .strip()
    )
    return s

def standardize(df: pd.DataFrame, name: str) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).replace("\ufeff", "").strip() for c in df.columns]

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(
            f"[{name}] Missing required columns: {missing}\n"
            f"[{name}] Found columns: {list(df.columns)}"
        )

    for c in ["WB_NAME", "Group", "species"]:
        df[c] = df[c].map(normalize_text)

    # treat missing Group consistently
    df["Group"] = df["Group"].fillna("Unknown")

    # drop rows missing keys
    df = df.dropna(subset=["WB_NAME", "species"])

    return df[["WB_NAME", "Group", "species"]]

# ============================================================
# COUNTS + COMPARE
# ============================================================
def species_counts(df: pd.DataFrame, label: str) -> pd.DataFrame:
    return (
        df.groupby(["WB_NAME", "Group"], as_index=False)["species"]
          .nunique()
          .rename(columns={"species": f"n_species_{label}"})
    )

def compare_counts(cnt_a: pd.DataFrame, cnt_b: pd.DataFrame) -> pd.DataFrame:
    cmp = cnt_a.merge(cnt_b, on=["WB_NAME", "Group"], how="outer", indicator=True)
    cmp["n_species_A"] = cmp["n_species_A"].fillna(0).astype(int)
    cmp["n_species_B"] = cmp["n_species_B"].fillna(0).astype(int)
    cmp["diff"] = cmp["n_species_A"] - cmp["n_species_B"]
    cmp["consistent"] = cmp["diff"].eq(0)
    return cmp

# ============================================================
# RUN
# ============================================================
df_a_raw = read_csv_safely(TABLE_A)
df_b_raw = read_csv_safely(TABLE_B)

df_a = standardize(df_a_raw, "Table_A (intersection)")
df_b = standardize(df_b_raw, "Table_B (ArcGIS)")

# ---- APPLY MANUAL COUNTRY NAME FIXES (key step) ----
df_b["WB_NAME"] = df_b["WB_NAME"].replace(NAME_MAP)

# Recompute after name fixes
cnt_a = species_counts(df_a, "A")
cnt_b = species_counts(df_b, "B")
cmp = compare_counts(cnt_a, cnt_b)

total_pairs = len(cmp)
n_consistent = int(cmp["consistent"].sum())
n_inconsistent = total_pairs - n_consistent

print("\n================ COMPARISON SUMMARY ================")
print(f"Total (country, group) pairs compared: {total_pairs}")
print(f"Consistent pairs: {n_consistent}")
print(f"Inconsistent pairs: {n_inconsistent}")

mismatches = cmp.loc[~cmp["consistent"]].sort_values(["WB_NAME", "Group"])
if mismatches.empty:
    print("\n✅ All (country, group) species counts are consistent after NAME_MAP fixes.")
else:
    print("\n❌ Still mismatches (first 50):")
    print(mismatches.head(50).to_string(index=False))

os.makedirs(os.path.dirname(OUT_COMPARE), exist_ok=True)
cmp.sort_values(["WB_NAME", "Group"]).to_csv(OUT_COMPARE, index=False, encoding="utf-8")
print(f"\nWrote full comparison to:\n{OUT_COMPARE}")
