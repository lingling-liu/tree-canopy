import os
import rasterio
import numpy as np

def process_raster(input_path, output_path, nodata_value):
    with rasterio.open(input_path) as src:
        data = src.read(1)  # Read the first band
        profile = src.profile
        
        # Replace inf with NoData value
        data[np.isinf(data)] = nodata_value
        
        # Update profile with NoData value
        profile.update(nodata=nodata_value)
        
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(data, 1)

def process_all_rasters(input_folder, output_folder, nodata_value):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('.tif'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            process_raster(input_path, output_path, nodata_value)
            print(f"Processed {filename}")

# Paths to the input and output folders
input_folder = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Stormwater\output\key_outputs\05072025"

# Create output directory for masked rasters
output_raster_dir = os.path.join(input_folder, "Processed")
os.makedirs(output_raster_dir, exist_ok=True)

# Define the NoData value (commonly -9999 or any other appropriate value for your data)
nodata_value = -9999

# Process all rasters in the folder
process_all_rasters(input_folder, output_raster_dir, nodata_value)
