import rasterio
import numpy as np

# Input and output paths
input_path = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Stormwater\chir1_annual_preciptation_climate_2009_2023_resize.tif"
output_path = input_path.replace(".tif", "_constant_value.tif")

# Open the single-band raster
with rasterio.open(input_path) as src:
    data = src.read(1)
    nodata = src.nodata

    # Mask nodata values before computing mean
    if nodata is not None:
        valid_data = data[data != nodata]
    else:
        valid_data = data

    mean_value = np.mean(valid_data)

    # Create a constant raster with the same shape and metadata
    constant_data = np.full_like(data, mean_value, dtype=np.float32)

    # Update metadata
    out_meta = src.meta.copy()
    out_meta.update({
        "dtype": "float32",
        "count": 1
    })

# Save the constant raster
with rasterio.open(output_path, "w", **out_meta) as dst:
    dst.write(constant_data, 1)

print(f"Saved constant-value raster to: {output_path}")
