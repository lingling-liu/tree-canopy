import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# File paths
file1 = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\Pollination\06-26-2024\pollinator_abundance_general_annual_NLCD_tree.tif"
file2 = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\Pollination\06-26-2024\pollinator_abundance_general_annual_NLCD.tif"

# Open the raster files
with rasterio.open(file1) as src1:
    raster1 = src1.read(1)
    profile = src1.profile

with rasterio.open(file2) as src2:
    raster2 = src2.read(1)

# Ensure both rasters have the same shape
if raster1.shape != raster2.shape:
    raise ValueError("The rasters do not have the same dimensions")

# Valid value range (adjust as needed for pollination data)
valid_min = 0
valid_max = 0.28

# Mask the values outside the valid range
mask = (raster1 >= valid_min) & (raster1 <= valid_max) & (raster2 >= valid_min) & (raster2 <= valid_max)

# Calculate the difference
difference = np.where(mask, raster1 - raster2, np.nan)

# Remove NaN values for min and max calculation
valid_diff = difference[~np.isnan(difference)]

# Compute min and max values
min_val = np.min(valid_diff)
max_val = np.max(valid_diff)
print(min_val)
print(max_val)

# Define the colormap
cmap = ListedColormap(plt.cm.Greens(np.linspace(0, 1, 256)))

# Save the difference raster
output_file = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\Pollination\06-26-2024\pollinator_abundance_difference.tif"
with rasterio.open(output_file, 'w', **profile) as dst:
    dst.write(difference, 1)

# Plot the difference raster
plt.figure(figsize=(5, 5))
plt.imshow(difference, cmap='Greens', vmin=min_val, vmax=max_val)
plt.colorbar(label='Pollinator Abundance Difference')
plt.title('Increase in Pollinator Abundance')
plt.axis('off')  # Remove the x and y axis
plt.show()

# Plot the histogram of pollinator abundance differences
plt.figure(figsize=(5, 5))
counts, bins, patches = plt.hist(valid_diff, bins=50, color='blue', alpha=0.7)
# plt.title('Histogram of Pollinator Abundance Differences')
plt.xlabel('Pollinator Abundance Difference', fontsize=16)
plt.ylabel('Number of Pixels', fontsize=16)  # Changed ylabel to 'Number of Pixels'
plt.xticks(fontsize=12)  # Set x-tick font size
plt.yticks(fontsize=12)  # Set y-tick font size
plt.grid(False)  # Remove grid lines

# Save histogram
histogram_output_file = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\Figure\pollinator_abundance_difference_histogram.png"
plt.savefig(histogram_output_file, dpi=300, bbox_inches='tight')

plt.show()