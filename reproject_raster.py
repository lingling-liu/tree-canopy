import os
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np

def reproject_raster(src_path, ref_path, dst_path):
    with rasterio.open(ref_path) as ref:
        ref_crs = ref.crs
        ref_transform = ref.transform
        ref_width = ref.width
        ref_height = ref.height
        ref_bounds = ref.bounds
        ref_data = ref.read(1)
        ref_nodata = ref.nodata

    with rasterio.open(src_path) as src:
        src_crs = src.crs
        src_transform = src.transform
        src_data = src.read(1)
        src_nodata = src.nodata

        # Handle case where nodata is None and ensure nodata is within valid range
        if src_nodata is None:
            if src_data.dtype == np.uint8:
                src_nodata = 255
            elif src_data.dtype == np.uint16:
                src_nodata = 65535
            elif np.issubdtype(src_data.dtype, np.floating):
                src_nodata = np.nan
            else:
                src_nodata = -9999  # Use an appropriate default for other types

        # Calculate the transform and dimensions of the output raster
        transform, width, height = calculate_default_transform(
            src_crs, ref_crs, src.width, src.height, *src.bounds, dst_width=ref_width, dst_height=ref_height
        )

        # Initialize the output array with nodata values
        output_data = np.full((ref_height, ref_width), src_nodata, dtype=src_data.dtype)

        # Reproject the source raster to match the reference raster
        reproject(
            source=src_data,
            destination=output_data,
            src_transform=src_transform,
            src_crs=src_crs,
            dst_transform=ref_transform,
            dst_crs=ref_crs,
            resampling=Resampling.nearest
        )

        # Apply the reference data as a mask
        mask = (ref_data == ref_nodata) | (ref_data < 0) | (ref_data > 1)
        output_data[mask] = src_nodata

        # Write the reprojected data to a new file
        with rasterio.open(
            dst_path, 'w',
            driver='GTiff',
            height=ref_height,
            width=ref_width,
            count=1,
            dtype=output_data.dtype,
            crs=ref_crs,
            transform=ref_transform,
            nodata=src_nodata
        ) as dst:
            dst.write(output_data, 1)

# Set paths
src_folder = r'D:\Shared drives\Urban Workflow\Data\Urban_LTER\Stormwater\Land_cover_updated_GEE'
ref_raster_path = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\Stormwater\output\runoff_ratio_NLCD_1.tif"
dst_folder = r'D:\Shared drives\Urban Workflow\Data\Urban_LTER\Stormwater\Land_cover_updated_GEE\reprojected'

# Create the destination folder if it does not exist
os.makedirs(dst_folder, exist_ok=True)

# Loop through the files in the source directory
for filename in os.listdir(src_folder):
    if filename.endswith('.tif'):  # Only process .tif files
        src_raster_path = os.path.join(src_folder, filename)
        dst_raster_path = os.path.join(dst_folder, filename)
        
        reproject_raster(src_raster_path, ref_raster_path, dst_raster_path)
        print(f'Reprojected {filename} and saved to {dst_raster_path}')
