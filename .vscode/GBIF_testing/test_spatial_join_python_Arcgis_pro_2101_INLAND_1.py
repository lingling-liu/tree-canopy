import pandas as pd

csv_arc = r"C:\Users\liu02034\Downloads\bacth_2101_SJ_Arcgis_Pro_inland.csv"
df = pd.read_csv(csv_arc, encoding="cp1252")

print("Has 'columnella magna' in species column?",
      (df["species"].astype(str).str.strip().str.lower() == "columnella magna").sum())

print(df[df["species"].astype(str).str.strip().str.lower() == "columnella magna"][["species","Group","WB_NAME"]].head(20))
