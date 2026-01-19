import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import os

# ---------------------------------------------------
# 1. File paths
# ---------------------------------------------------
shapefile_path = r"G:\Shared drives\Urban Workflow\Data\Pollination\ESA_2024\SVI2022_MINNES_Pairwise_TCMA_poverty_deviation_updated.shp"

output_folder = r"G:\Shared drives\Urban Workflow\Data\Pollination\ESA_2024\Figure"
os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(output_folder, "Figure_poverty_deviation.png")

# ---------------------------------------------------
# 2. Read shapefile
# ---------------------------------------------------
gdf = gpd.read_file(shapefile_path)

print("Columns:")
print(gdf.columns)

# ---------------------------------------------------
# 4. Plot settings
# ---------------------------------------------------
vmin, vmax = -1.0, 1.0
cmap = "seismic_r"   # alternatives: "RdBu_r", "coolwarm", "bwr"

# ---------------------------------------------------
# 5. Create figure
# ---------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 6))

# ---------------------------------------------------
# 6. Plot polygons
# ---------------------------------------------------
gdf.plot(
    column="Poverty_dv",
    cmap=cmap,
    vmin=vmin,
    vmax=vmax,
    linewidth=0,
    edgecolor="none",
    ax=ax,
    aspect="equal"    # prevents GeoPandas aspect error
)

# ---------------------------------------------------
# 7. Boundary outline
# ---------------------------------------------------
gdf.boundary.plot(
    ax=ax,
    color="black",
    linewidth=0.5
)

# ---------------------------------------------------
# 8. Axis formatting
# ---------------------------------------------------
ax.set_axis_off()

# ---------------------------------------------------
# 9. Colorbar
# ---------------------------------------------------
norm = Normalize(vmin=vmin, vmax=vmax)
sm = ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])

cbar = fig.colorbar(
    sm,
    ax=ax,
    fraction=0.035,
    pad=0.02
)
cbar.set_label("Poverty Deviation", fontsize=12)

# ---------------------------------------------------
# 10. Save output
# ---------------------------------------------------
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches="tight")
print("Saved figure to:", output_file)

plt.show()
plt.close(fig)
