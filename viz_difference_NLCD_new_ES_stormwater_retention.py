import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# File paths
file1 = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\Stormwater\output\key_outputs\Processed\retention_volume_NLCD_tree_2.tif"
file2 = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\Stormwater\output\key_outputs\Processed\retention_volume_NLCD_2.tif"

# Open the raster files
with rasterio.open(file1) as src1:
    raster1 = src1.read(1)
    profile = src1.profile

with rasterio.open(file2) as src2:
    raster2 = src2.read(1)

# Ensure both rasters have the same shape
if raster1.shape != raster2.shape:
    raise ValueError("The rasters do not have the same dimensions")

# Valid value range (adjust as needed for retention volume data)
valid_min = 130
valid_max = 730

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
cmap = ListedColormap(plt.cm.Blues(np.linspace(0, 1, 256)))

# Save the difference raster
output_file = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\Stormwater\output\key_outputs\Processed\retention_volume_difference.tif"
with rasterio.open(output_file, 'w', **profile) as dst:
    dst.write(difference, 1)

# Plot the difference raster
plt.figure(figsize=(5, 5))
plt.imshow(difference, cmap='Blues', vmin=min_val, vmax=max_val)
plt.colorbar(label='Retention Volume Difference')
plt.title('Increase in Retention Volume')
plt.axis('off')  # Remove the x and y axis
plt.show()

# Plot the histogram of retention volume differences
plt.figure(figsize=(5, 5))
counts, bins, patches = plt.hist(valid_diff, bins=50, color='blue', alpha=0.7)
plt.title('Histogram of Retention Volume Differences')
plt.xlabel('Retention Volume Difference')
plt.ylabel('Number of Pixels')  # Changed ylabel to 'Number of Pixels'
plt.grid(False)  # Remove grid lines
plt.show()

# Print the sum of counts to verify
print("Sum of counts in all bins:", np.sum(counts))
