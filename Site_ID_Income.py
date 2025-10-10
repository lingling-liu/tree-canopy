import pandas as pd

# Base folder path
base_folder = r"G:\Shared drives\Urban Workflow\Data\Pollination\Site_ID_index"

# File paths
site_info_path = f"{base_folder}\\LTER_BeeLawn_SiteID_information.xlsx"
income_info_path = f"{base_folder}\\Site_ID_Income.xlsx"
output_path = f"{base_folder}\\Updated_LTER_BeeLawn_SiteID_with_MedianIncome.xlsx"

# Load the data
site_df = pd.read_excel(site_info_path)
income_df = pd.read_excel(income_info_path)

# Optional: check column names to verify the common key and income column
print("Site file columns:", site_df.columns)
print("Income file columns:", income_df.columns)

# Merge on 'Sampling_Position'
merged_df = site_df.merge(income_df[['Sampling_Position', 'MEDIANHHI']], on='Sampling_Position', how='left')

# Save to new Excel file
merged_df.to_excel(output_path, index=False)

print(f"Updated table saved to: {output_path}")
