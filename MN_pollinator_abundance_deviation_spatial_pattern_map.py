import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import os

# 1. File path
shapefile_path = r"G:\Shared drives\Urban Workflow\Data\Pollination\ESA_2024\SVI2022_MINNES_Pairwise_TCMA_Pollinator_abundance.shp"
# 2. Output folder + filename
output_folder = r"G:\Shared drives\Urban Workflow\Data\Pollination\ESA_2024\Figure"
output_file = os.path.join(output_folder, "Figure_pollination_abundance_deviation.png")

# 3. Read shapefile
gdf = gpd.read_file(shapefile_path)
print(gdf.columns)

# 4. Filter valid values
gdf = gdf[gdf["mean_dev1"] != -999]

# 5. Plot settings
vmin, vmax = -1.0, 1.0
cmap = "seismic_r"      # red → white → blue

# 6. Create figure (size 6x6)
fig, ax = plt.subplots(figsize=(6, 6))

# 7. Plot polygons
gdf.plot(
    column="mean_dev1",
    cmap=cmap,
    vmin=vmin,
    vmax=vmax,
    linewidth=0,
    edgecolor="none",
    ax=ax
)

# 8. Boundary outline
gdf.boundary.plot(
    ax=ax,
    color="black",
    linewidth=0.5
)

# 9. Remove axis
ax.set_axis_off()

# 10. Colorbar
norm = Normalize(vmin=vmin, vmax=vmax)
sm = ScalarMappable(norm=norm, cmap=cmap)
sm._A = []

cbar = fig.colorbar(sm, ax=ax, fraction=0.035, pad=0.02)
cbar.set_label("Pollinator Abundance Deviation", fontsize=12)

plt.tight_layout()

# 11. Save figure
plt.savefig(output_file, dpi=300, bbox_inches="tight")
print("Saved figure to:", output_file)

plt.show()
