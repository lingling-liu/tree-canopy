import rasterio
import numpy as np
import pygeoprocessing

# File paths
diff_file = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Urban_cooling\Minneapolis\temp_06_19_2024\resize\T_air_difference_raster.tif"
landcover_file = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Stormwater\Land_cover_updated_GEE\reprojected\NLCD_adding_tree_TCMA.tif"

aligned_diff_file = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Urban_cooling\Minneapolis\temp_06_19_2024\aligned_diff.tif"
aligned_lulc_file = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Urban_cooling\Minneapolis\temp_06_19_2024\aligned_lulc.tif"

# Get target pixel size from the difference raster
diff_info = pygeoprocessing.get_raster_info(diff_file)
target_pixel_size = diff_info['pixel_size']

# Align and resize both rasters
pygeoprocessing.align_and_resize_raster_stack(
    [diff_file, landcover_file],
    [aligned_diff_file, aligned_lulc_file],
    ['near', 'near'],
    target_pixel_size,
    'intersection',
    raster_align_index=0
)

# Read aligned rasters
with rasterio.open(aligned_diff_file) as diff_src, rasterio.open(aligned_lulc_file) as lc_src:
    diff = diff_src.read(1).astype(float)
    lc = lc_src.read(1).astype(int)

    # Handle NoData values
    diff_nodata = diff_src.nodata
    lc_nodata = lc_src.nodata

    diff_mask = (diff != diff_nodata) if diff_nodata is not None else np.full(diff.shape, True)
    lc_mask = (lc != lc_nodata) if lc_nodata is not None else np.full(lc.shape, True)
    valid_mask = diff_mask & lc_mask

    # Filter for 3-digit LULC codes, EXCLUDING 400–499
    is_3digit = (lc >= 100) & (lc <= 999) & ~((lc >= 400) & (lc < 500))
    canopy_class = lc % 10  # last digit: 1 = low, 2 = medium, 3 = high

    # Compute mean difference for each canopy class
    results = {}
    for canopy_value in [1, 2, 3]:
        class_mask = (canopy_class == canopy_value) & is_3digit & valid_mask
        count = np.sum(class_mask)

        if count > 0:
            mean_diff = np.nanmean(diff[class_mask])
            results[f"Tree canopy class {canopy_value}"] = f"{mean_diff:.4f} °C ({count} pixels)"
        else:
            results[f"Tree canopy class {canopy_value}"] = "No valid pixels"

# Print results
for k, v in results.items():
    print(f"{k}: Mean temperature difference = {v}")
