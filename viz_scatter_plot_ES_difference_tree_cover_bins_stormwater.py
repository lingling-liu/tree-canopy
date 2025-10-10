import pygeoprocessing
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import resample
import pandas as pd
import os

# Input files
diff_file = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Stormwater\output\key_outputs\05072025\Processed\retention_volume_difference_05112025.tif"
canopy_file = r"G:\Shared drives\Urban Workflow\Data\Tree\Smoothed_Canopy_500m_Valid.tif"

# Aligned output files
aligned_diff_file = os.path.splitext(diff_file)[0] + "_aligned.tif"
aligned_canopy_file = os.path.splitext(canopy_file)[0] + "_aligned.tif"

# Get target pixel size from the difference raster
diff_info = pygeoprocessing.get_raster_info(diff_file)
target_pixel_size = diff_info['pixel_size']

# Align and resize both rasters to match the diff_file
print("Aligning rasters...")
pygeoprocessing.align_and_resize_raster_stack(
    [diff_file, canopy_file],
    [aligned_diff_file, aligned_canopy_file],
    ['near', 'near'],
    target_pixel_size,
    'intersection',
    raster_align_index=0
)

# Open the aligned rasters
print("Reading aligned rasters...")
with rasterio.open(aligned_canopy_file) as src1, rasterio.open(aligned_diff_file) as src2:
    canopy = src1.read(1)
    retention_diff = src2.read(1)

    if canopy.shape != retention_diff.shape:
        raise ValueError("The aligned rasters do not have the same shape")
    if src1.transform != src2.transform:
        raise ValueError("The aligned rasters do not have the same geotransform")

# Mask: valid values and canopy > 0
print("Masking invalid values and filtering canopy > 0...")
mask = (~np.isnan(canopy)) & (~np.isnan(retention_diff)) & (canopy > 0)

# Flatten and apply mask
canopy_vals = canopy[mask].flatten()
retention_diff_vals = retention_diff[mask].flatten()

# Sample 20,000 points
print("Sampling 20,000 points...")
sample_size = min(20000, len(canopy_vals))
canopy_sample, retention_sample = resample(
    canopy_vals, retention_diff_vals, n_samples=sample_size, random_state=42
)

# Bin canopy into 5% intervals
print("Binning canopy values...")
bins = np.arange(0, 105, 5)
bin_labels = [f"{bins[i]}–{bins[i+1]}" for i in range(len(bins) - 1)]
bin_indices = np.digitize(canopy_sample, bins) - 1

# Create DataFrame for binning and averaging
bin_df = pd.DataFrame({
    'CanopyBin': bin_indices,
    'CanopyLabel': [bin_labels[i] if 0 <= i < len(bin_labels) else "Out of Range" for i in bin_indices],
    'RetentionDiff': retention_sample
})
grouped = bin_df.groupby('CanopyLabel').mean(numeric_only=True).reindex(bin_labels)

# Plot both scatter and binned average line
print("Plotting results...")
plt.figure(figsize=(6, 6))
plt.rcParams.update({'font.size': 14})

plt.scatter(canopy_sample, retention_sample, alpha=0.2, s=10, label='Sample Points')
plt.plot(bins[:-1] + 2.5, grouped['RetentionDiff'], color='red', lw=2, marker='o', label='Average per 5% Bin')
plt.xlabel("Tree Canopy % (within 500m)")
plt.ylabel("Stormwater Retention Volume Difference (m³)")
plt.title("Retention Volume Difference vs. Tree Canopy %",fontsize=12)
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save the figure
output_path = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Figure\retention_diff_vs_canopy_05122025.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300)
plt.show()
