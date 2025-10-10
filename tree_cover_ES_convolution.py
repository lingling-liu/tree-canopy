import numpy as np
import rasterio
from scipy.ndimage import convolve
import pygeoprocessing
import matplotlib.pyplot as plt

# Paths
canopy_file = r"G:\Shared drives\Urban Workflow\Data\Tree\Tree_canopy_NASA_30m_MN_UTM_re.tif"
nlcd_file = r"G:\Shared drives\Urban Workflow\Data\Tree\NLCD_2016_Land_Cover_clip_tcma_tree_canopyr.tif"
aligned_canopy_file = r"G:\Shared drives\Urban Workflow\Data\Tree\aligned_canopy.tif"
aligned_nlcd_file = r"G:\Shared drives\Urban Workflow\Data\Tree\aligned_nlcd.tif"
output_file = r"G:\Shared drives\Urban Workflow\Data\Tree\Smoothed_Canopy_500m_Valid.tif"

# Step 1: Align canopy and NLCD
canopy_info = pygeoprocessing.get_raster_info(canopy_file)
target_pixel_size = canopy_info['pixel_size']

pygeoprocessing.align_and_resize_raster_stack(
    [canopy_file, nlcd_file],
    [aligned_canopy_file, aligned_nlcd_file],
    ['near', 'near'],
    target_pixel_size,
    'intersection',
    raster_align_index=0  # Align to canopy raster
)

# Step 2: Read aligned rasters
with rasterio.open(aligned_canopy_file) as canopy_src, rasterio.open(aligned_nlcd_file) as nlcd_src:
    canopy = canopy_src.read(1)
    nlcd = nlcd_src.read(1)
    profile = canopy_src.profile

# Step 3: Mask invalid land cover types (11 = water, 12 = snow/ice)
canopy = np.clip(canopy, 0, 100)
invalid_mask = np.isin(nlcd, [11, 12])
valid_mask = ~invalid_mask

# Temporarily mask invalids as NaN for smoothing
canopy_masked = canopy.copy().astype(float)
canopy_masked[invalid_mask] = np.nan

# Step 4: Smooth using 500m convolution (17x17 kernel)
kernel_size = 17
kernel = np.ones((kernel_size, kernel_size), dtype=float)
kernel /= kernel.sum()

filled = np.nan_to_num(canopy_masked, nan=0.0)
weights = convolve(valid_mask.astype(float), kernel, mode='nearest')
smoothed = convolve(filled, kernel, mode='nearest') / np.maximum(weights, 1e-6)

# Step 5: Set NLCD 11/12 areas to 0 in final output
smoothed[invalid_mask] = 0.0

# Step 6: Save to GeoTIFF
profile.update(dtype=rasterio.float32, nodata=None)
with rasterio.open(output_file, 'w', **profile) as dst:
    dst.write(smoothed.astype(np.float32), 1)

print(f"Smoothed tree canopy saved to: {output_file}")

# Optional: Quick visual check
plt.figure(figsize=(10, 5))
plt.imshow(smoothed, cmap='viridis')
plt.colorbar(label='Smoothed Tree Canopy (%)')
plt.title('Smoothed Canopy with NLCD 11/12 = 0')
plt.axis('off')
plt.tight_layout()
plt.show()
