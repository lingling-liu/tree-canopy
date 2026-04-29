import os
import glob
import pandas as pd

# -----------------------------
# Settings
# -----------------------------
per_batch_dir = r"E:\FInal\N_species\polygons\species_by_inland10km\per_batch"

targets = [
    "Curaçao (Neth.)",
    "Côte d'Ivoire",
    "São Tomé and Príncipe",
    "Saint-Barthélemy (Fr.)",
]

# Output report
out_report = os.path.join(per_batch_dir, "_country_name_file_hits_inland10km.csv")

# Column that contains country name in your per-batch outputs
COUNTRY_COL = "WB_NAME"

# -----------------------------
# Scan files
# -----------------------------
rows = []
csvs = sorted(glob.glob(os.path.join(per_batch_dir, "*.csv")))

if not csvs:
    raise FileNotFoundError(f"No CSVs found in: {per_batch_dir}")

print(f"📁 Found {len(csvs)} CSV files to scan.\n")

for i, fp in enumerate(csvs, 1):
    fname = os.path.basename(fp)
    print(f"🔍 [{i}/{len(csvs)}] Scanning: {fname}")

    try:
        df = pd.read_csv(fp, usecols=[COUNTRY_COL])
    except ValueError:
        # COUNTRY_COL not found
        rows.append({
            "file": fname,
            "status": f"missing_column:{COUNTRY_COL}",
            "found_names": "",
            "total_matches": 0,
        })
        print(f"   ⚠️  Skipped (missing column {COUNTRY_COL})")
        continue
    except Exception as e:
        rows.append({
            "file": fname,
            "status": f"read_error:{repr(e)}",
            "found_names": "",
            "total_matches": 0,
        })
        print(f"   ❌ Read error: {repr(e)}")
        continue

    found = []
    total_matches = 0

    # Make sure country col is string-ish
    s = df[COUNTRY_COL].astype("string")

    for name in targets:
        n = int((s == name).sum())
        if n > 0:
            found.append(f"{name} ({n})")
            total_matches += n

    if found:
        print(f"   ✅ HIT → {fname}")
        for f in found:
            print(f"      - {f}")

        rows.append({
            "file": fname,
            "status": "hit",
            "found_names": "; ".join(found),
            "total_matches": total_matches,
        })
    else:
        print(f"   ⏭️  No target country names found.")

# -----------------------------
# Save report
# -----------------------------
report = pd.DataFrame(rows).sort_values(["status", "file"])
report.to_csv(out_report, index=False, encoding="utf-8-sig")

print("\n" + "=" * 60)
print(f"✅ Done. Report saved to:\n{out_report}")

if len(report) == 0:
    print("\n🎉 No files contained any of the target country names.")
else:
    print("\n📌 Files that contained target country names:")
    print(report[report["status"] == "hit"][["file", "found_names", "total_matches"]])

print("\nTop hits preview:")
print(report.head(30))
