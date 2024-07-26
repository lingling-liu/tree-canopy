import os
import rasterio
import numpy as np

def process_raster(input_path, output_path, nodata_value, mask_data):
    with rasterio.open(input_path) as src:
        data = src.read(1)  # Read the first band
        profile = src.profile
        
        # Apply the mask
        mask = np.isin(mask_data, [21, 22, 23, 24])
        data[~mask] = nodata_value
        
        # Replace inf with NoData value
        data[np.isinf(data)] = nodata_value
        
        # Update profile with NoData value
        profile.update(nodata=nodata_value)
        
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(data, 1)

def process_all_rasters(input_folder, output_folder, nodata_value, mask_path):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    with rasterio.open(mask_path) as mask_src:
        mask_data = mask_src.read(1)  # Read the first band of the mask

    for filename in os.listdir(input_folder):
        if filename.endswith('.tif'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            process_raster(input_path, output_path, nodata_value, mask_data)
            print(f"Processed {filename}")

# Paths to the input and output folders and mask file
input_folder = r'D:\Shared drives\Urban Workflow\Data\Urban_LTER\Stormwater\output\key_outputs\Processed'
output_folder = r'D:\Shared drives\Urban Workflow\Data\Urban_LTER\Stormwater\output\key_outputs\Processed\Processed_with_NoData'
mask_path = r'D:\Shared drives\Urban Workflow\Data\Urban_LTER\Stormwater\Land_cover_updated_GEE\reprojected\NLCD_2016_30m_TCMA.tif'

# Define the NoData value (commonly -9999 or any other appropriate value for your data)
nodata_value = -9999

# Process all rasters in the folder
process_all_rasters(input_folder, output_folder, nodata_value, mask_path)
