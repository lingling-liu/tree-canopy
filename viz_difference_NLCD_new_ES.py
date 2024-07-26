import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# File paths
file1 = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\Urban_cooling\Minneapolis\temp_06_19_2024\T_air_NLCD_tree_02.tif"
file2 = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\Urban_cooling\Minneapolis\temp_06_19_2024\T_air_NLCD_02.tif"

# Open the raster files
with rasterio.open(file1) as src1:
    raster1 = src1.read(1)
    profile = src1.profile

with rasterio.open(file2) as src2:
    raster2 = src2.read(1)

# Ensure both rasters have the same shape
if raster1.shape != raster2.shape:
    raise ValueError("The rasters do not have the same dimensions")

# Valid value range
valid_min = 22
valid_max = 26

# Mask the values outside the valid range
mask = (raster1 >= valid_min) & (raster1 <= valid_max) & (raster2 >= valid_min) & (raster2 <= valid_max)

# Calculate the difference
difference = np.where(mask, raster1 - raster2, np.nan)

# Remove NaN values for min and max calculation
valid_diff = difference[~np.isnan(difference)]

# Compute min and max values
min_val = np.min(valid_diff)
max_val = np.max(valid_diff)

# Reverse the colormap
cmap = ListedColormap(plt.cm.RdYlBu_r(np.linspace(0, 1, 256)))

# Save the difference raster
output_file = "D:\\Shared drives\\Urban Workflow\\Data\\Urban_LTER\\Urban_cooling\\Minneapolis\\temp_06_19_2024\\resize\T_air_difference_raster.tif"
with rasterio.open(output_file, 'w', **profile) as dst:
    dst.write(difference, 1)

# Plot the difference raster
plt.figure(figsize=(5, 5))
plt.imshow(difference, cmap='Greens_r', vmin=min_val, vmax=max_val)
plt.colorbar(label='Temperature Difference')
plt.title('Reducded Temperature after adding tree')
plt.axis('off')  # Remove the x and y axis
plt.show()

# Plot the histogram heatmap
plt.figure(figsize=(5, 5))
plt.hist(valid_diff, bins=50, color='blue', alpha=0.7)
# plt.title('Histogram of Temperature Differences', fontsize=20)
plt.xlabel('Temperature Difference', fontsize=16)
plt.ylabel('Frequency', fontsize=16)
plt.xticks(fontsize=12)  # Set x-tick font size
plt.yticks(fontsize=12)  # Set y-tick font size
plt.grid(False)  # Remove grid lines

# Save histogram
histogram_output_file = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\Figure\T_air_difference_histogram.png"
plt.savefig(histogram_output_file, dpi=300, bbox_inches='tight')

plt.show()