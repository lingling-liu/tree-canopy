import numpy as np
import matplotlib.pyplot as plt
import rasterio
import pygeoprocessing

# Input files
canopy_file = r"G:\Shared drives\Urban Workflow\Data\Tree\Tree_canopy_NASA_30m_MN_UTM_re.tif"
nlcd_file = r"G:\Shared drives\Urban Workflow\Data\Tree\NLCD_2016_Land_Cover_clip_tcma_tree_canopyr.tif"

# Aligned output files
aligned_canopy_file = r"G:\Shared drives\Urban Workflow\Data\Tree\aligned_tree_canopy.tif"
aligned_nlcd_file = r"G:\Shared drives\Urban Workflow\Data\Tree\aligned_nlcd.tif"

# Step 1: Align canopy and NLCD
canopy_info = pygeoprocessing.get_raster_info(canopy_file)
target_pixel_size = canopy_info['pixel_size']

pygeoprocessing.align_and_resize_raster_stack(
    [canopy_file, nlcd_file],
    [aligned_canopy_file, aligned_nlcd_file],
    ['near', 'near'],
    target_pixel_size,
    'intersection',
    raster_align_index=0
)

# Step 2: Read aligned rasters
with rasterio.open(aligned_canopy_file) as canopy_src, rasterio.open(aligned_nlcd_file) as nlcd_src:
    canopy = canopy_src.read(1)
    nlcd = nlcd_src.read(1)

# Step 3: Define target NLCD classes
target_classes = [21, 22, 23, 24]
class_labels = {
    21: "Developed, Open Space",
    22: "Developed, Low Intensity",
    23: "Developed, Medium Intensity",
    24: "Developed, High Intensity"
}

# Step 4: Set up combined figure
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
bins = np.arange(0, 105, 5)
fontsize = 14

for idx, nlcd_class in enumerate(target_classes):
    ax = axes[idx // 2, idx % 2]
    mask = (nlcd == nlcd_class) & (canopy >= 0)
    canopy_values = canopy[mask]

    if canopy_values.size == 0:
        print(f"No data for NLCD class {nlcd_class}")
        continue

    counts, bin_edges = np.histogram(canopy_values, bins=bins)
    percentages = (counts / counts.sum()) * 100

    ax.bar(bin_edges[:-1], percentages, width=5, align='edge', edgecolor='black')
    ax.set_title(class_labels[nlcd_class], fontsize=fontsize)
    ax.set_xlabel("Tree Canopy Cover (%)", fontsize=fontsize)
    ax.set_ylabel("Pixel Percentage (%)", fontsize=fontsize)
    ax.set_xticks(bins)
    ax.set_ylim(0, max(percentages) * 1.1)
    ax.tick_params(axis='both', labelsize=fontsize - 2)
    ax.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
output_path = r"G:\Shared drives\Urban Workflow\Data\Tree\Figures\canopy_histogram_2x2.png"
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Figure saved to: {output_path}")
