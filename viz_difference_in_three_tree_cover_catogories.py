import rasterio
import numpy as np

# File paths
diff_file = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Urban_cooling\Minneapolis\temp_06_19_2024\resize\T_air_difference_raster.tif"
landcover_file = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Stormwater\Land_cover_updated_GEE\reprojected\NLCD_adding_tree_TCMA.tif"

# Open rasters and read data
with rasterio.open(diff_file) as diff_src, rasterio.open(landcover_file) as lc_src:
    diff = diff_src.read(1).astype(float)
    lc = lc_src.read(1)

    # Check if raster shapes match
    if diff.shape != lc.shape:
        raise ValueError("The rasters do not have the same dimensions")

    # Handle NoData values
    diff_nodata = diff_src.nodata
    lc_nodata = lc_src.nodata

    diff_mask = (diff != diff_nodata) if diff_nodata is not None else np.full(diff.shape, True)
    lc_mask = (lc != lc_nodata) if lc_nodata is not None else np.full(lc.shape, True)

    valid_mask = diff_mask & lc_mask
    diff_masked = np.where(valid_mask, diff, np.nan)

    # Extract last digit to identify canopy class
    canopy_class = lc % 10

    results = {}
    for canopy_value in [1, 2, 3]:
        class_mask = (canopy_class == canopy_value) & valid_mask
        count = np.sum(class_mask)

        if count > 0:
            mean_diff = np.nanmean(diff[class_mask])
            results[f"Tree canopy class {canopy_value}"] = f"{mean_diff:.4f} °C ({count} pixels)"
        else:
            results[f"Tree canopy class {canopy_value}"] = "No valid pixels"

# Print results
for k, v in results.items():
    print(f"{k}: Mean temperature difference = {v}")
