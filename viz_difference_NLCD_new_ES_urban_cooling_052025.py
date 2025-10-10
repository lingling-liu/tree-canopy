import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable

# File paths for Urban Cooling - Minneapolis
file1 = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Urban_cooling\Minneapolis\temp_06_19_2024\T_air_NLCD_tree_02.tif"
file2 = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Urban_cooling\Minneapolis\temp_06_19_2024\T_air_NLCD_02.tif"
output_raster = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Urban_cooling\Minneapolis\temp_06_19_2024\T_air_difference_05112025.tif"
output_diff_map = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Figure\052025\T_air_difference_map_05112025.png"
output_hist = r"G:\Shared drives\Urban Workflow\Data\Urban_LTER\Figure\052025\T_air_difference_histogram_05112025.png"

# Open the raster files
with rasterio.open(file1) as src1:
    raster1 = src1.read(1)
    profile = src1.profile

with rasterio.open(file2) as src2:
    raster2 = src2.read(1)

# Ensure both rasters have the same shape
if raster1.shape != raster2.shape:
    raise ValueError("The rasters do not have the same dimensions")

# Define valid temperature range (in °C, adjust if needed)
valid_min = 22
valid_max = 26

# Apply mask to retain valid values
mask = (raster1 >= valid_min) & (raster1 <= valid_max) & (raster2 >= valid_min) & (raster2 <= valid_max)

# Calculate temperature difference
difference = np.where(mask, raster1 - raster2, np.nan)

# Extract valid differences
valid_diff = difference[~np.isnan(difference)]

# Compute stats
min_val = np.min(valid_diff)
max_val = np.max(valid_diff)
print("Min:", min_val)
print("Max:", max_val)

# Save difference raster
with rasterio.open(output_raster, 'w', **profile) as dst:
    dst.write(difference, 1)

# Plot and save difference map
fig, ax = plt.subplots(figsize=(5, 5))
fig.subplots_adjust(right=0.82)
img = ax.imshow(difference, cmap='Greens_r', vmin=min_val, vmax=max_val)
ax.axis('off')

# Add colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.2)
cbar = plt.colorbar(img, cax=cax, shrink=0.5)

# Add title
fig.suptitle('Air Temperature Difference (°C)', fontsize=14, y=0.95)

plt.savefig(output_diff_map, dpi=300, bbox_inches='tight')
plt.show()

# Plot and save histogram
plt.figure(figsize=(5, 5))
plt.hist(valid_diff, bins=50, color='blue', alpha=0.7)
plt.xlabel('Air Temperature Difference (°C)', fontsize=16)
plt.ylabel('Number of Pixels', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Format y-axis
ax = plt.gca()
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((6, 6))
ax.yaxis.set_major_formatter(formatter)

plt.savefig(output_hist, dpi=300, bbox_inches='tight')
plt.show()
