import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# File paths
file1 = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\Carbon\06-26-2024\tot_c_cur_NLCD_tree.tif"
file2 = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\Carbon\06-26-2024\tot_c_cur_NLCD.tif"

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
valid_min = 0
valid_max = 5.1

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
output_file = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\Carbon\06-26-2024\carbon_difference_raster.tif"
with rasterio.open(output_file, 'w', **profile) as dst:
    dst.write(difference, 1)

# Plot the difference raster
plt.figure(figsize=(5, 5))
plt.imshow(difference, cmap='Greens', vmin=min_val, vmax=max_val)
plt.colorbar(label='Carbon Difference')
plt.title('Increased Carbon Storage after Adding Trees')
plt.axis('off')  # Remove the x and y axis
plt.show()

# Plot the histogram heatmap
plt.figure(figsize=(5, 5))
plt.hist(valid_diff, bins=50, color='blue', alpha=0.7)
plt.title('Histogram of Carbon Differences')
plt.xlabel('Carbon Difference')
plt.ylabel('Frequency')
plt.grid(False)  # Remove grid lines
plt.show()
