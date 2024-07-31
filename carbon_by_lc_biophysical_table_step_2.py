import os
import pandas as pd
import numpy as np
import rasterio
from osgeo import gdal

# Change the current working directory
new_directory = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\RS parameterization\biomass_SA\aligned"
os.chdir(new_directory)

# Define the LULC file path
lulc_file = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\RS parameterization\aligned_lulc.tif"

# List all biomass files in the directory
biomass_files = [f for f in os.listdir(new_directory) if f.endswith('.tif') and 'aligned_lulc' not in f]

# Read the LULC file
with rasterio.open(lulc_file) as src:
    lulc = src.read(1)
    profile = src.profile

# Get unique land cover classes from the LULC file
classes = np.unique(lulc)
print("Land cover classes:", classes)

# Initialize dictionaries to store the results
mean_bg_dict = {code: [] for code in classes}
mean_ag_dict = {code: [] for code in classes}

# Function to process biomass data
def process_biomass(biomass, code):
    mask = lulc == code
    a = biomass[mask]
    classified_values = a[(a > 0) & (a < 10000)]
    if classified_values.size > 0:
        mean_value = classified_values.mean()
        return mean_value
    else:
        return np.nan

# Process each biomass file
for biomass_file in biomass_files:
    biomass_path = os.path.join(new_directory, biomass_file)
    
    with rasterio.open(biomass_path) as src:
        biomass = src.read(1)

    for code in classes:
        if "belowground" in biomass_file.lower():
            mean_bg = process_biomass(biomass, code)
            if not np.isnan(mean_bg):
                mean_bg_dict[code].append(mean_bg)
        elif "aboveground" in biomass_file.lower():
            mean_ag = process_biomass(biomass, code)
            if not np.isnan(mean_ag):
                mean_ag_dict[code].append(mean_ag)

# Calculate the final mean values for each land cover class
final_results = {
    'Land_Cover_Class': [],
    'Mean_Belowground_Biomass': [],
    'Mean_Aboveground_Biomass': []
}

for code in classes:
    final_results['Land_Cover_Class'].append(code)
    final_results['Mean_Belowground_Biomass'].append(np.nanmean(mean_bg_dict[code])*1.10231/10 if mean_bg_dict[code] else np.nan)
    final_results['Mean_Aboveground_Biomass'].append(np.nanmean(mean_ag_dict[code])*1.10231/10 if mean_ag_dict[code] else np.nan)

# Convert the results to a DataFrame
results_df = pd.DataFrame(final_results)

# Define the output Excel file path
output_excel = os.path.join(new_directory, 'biomass_land_cover_statistics.xlsx')

# Write the DataFrame to an Excel file
results_df.to_excel(output_excel, index=False)

print(f"Results saved to {output_excel}")
