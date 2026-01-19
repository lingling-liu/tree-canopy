import os
import geopandas as gpd
import matplotlib.pyplot as plt

# ==================================================
# 0. Output directory
# ==================================================
out_dir = r"G:\Shared drives\Urban Workflow\Data\Pollination\ESA_2024\Figure"
os.makedirs(out_dir, exist_ok=True)

# ==================================================
# 1. File paths
# ==================================================
tcma_path = r"G:\Shared drives\Urban Workflow\Data\Pollination\ESA_2024\ESA_2024_pollination\mn_county_boundaries_TCMA.shp"
state_path = r"G:\Shared drives\Urban Workflow\Data\Pollination\ESA_2024\ESA_2024_pollination\state_of_minnesota.shp"

# ==================================================
# 2. Read shapefiles
# ==================================================
gdf_state = gpd.read_file(state_path)
gdf_tcma = gpd.read_file(tcma_path)

# Ensure CRS match
if gdf_state.crs != gdf_tcma.crs:
    gdf_tcma = gdf_tcma.to_crs(gdf_state.crs)

# ==================================================
# 3. Ramsey county subset (using CTY_NAME)
# ==================================================
COUNTY_COL = "CTY_NAME"
RAMSEY_NAME = "Ramsey"

gdf_ramsey = gdf_tcma[gdf_tcma[COUNTY_COL] == RAMSEY_NAME]
if gdf_ramsey.empty:
    raise ValueError("No features found for Ramsey with CTY_NAME == 'Ramsey'")

# TCMA bounds (for figure 2)
tcma_minx, tcma_miny, tcma_maxx, tcma_maxy = gdf_tcma.total_bounds

# ==================================================
# FIGURE 1: Minnesota with TCMA counties inside
# ==================================================
fig1, ax1 = plt.subplots(figsize=(10, 10))  # larger figure

# Minnesota background
gdf_state.plot(ax=ax1, color="#b9b3a9", edgecolor="none")

# Pad extent so Minnesota appears smaller
sxmin, symin, sxmax, symax = gdf_state.total_bounds
xpad = (sxmax - sxmin) * 0.35
ypad = (symax - symin) * 0.35
ax1.set_xlim(sxmin - xpad, sxmax + xpad)
ax1.set_ylim(symin - ypad, symax + ypad)

# TCMA counties
gdf_tcma.plot(
    ax=ax1,
    facecolor="#d2cec7",
    edgecolor="black",
    linewidth=1.4
)

# Ramsey highlighted
gdf_ramsey.plot(
    ax=ax1,
    facecolor="#b02a2a",
    edgecolor="black",
    linewidth=1.7
)

ax1.set_axis_off()
ax1.set_aspect("equal")

# Save figure 1 (PNG + SVG)
fig1_png = os.path.join(out_dir, "MN_TCMA_Ramsey.png")
fig1_svg = os.path.join(out_dir, "MN_TCMA_Ramsey.svg")
fig1.savefig(fig1_png, dpi=300, bbox_inches="tight")
fig1.savefig(fig1_svg, dpi=300, bbox_inches="tight")
plt.close(fig1)

# ==================================================
# FIGURE 2: TCMA only (7 counties), Ramsey highlighted and labeled
# ==================================================
fig2, ax2 = plt.subplots(figsize=(10, 10))  # larger figure

# TCMA counties
gdf_tcma.plot(
    ax=ax2,
    facecolor="#f4f4f0",
    edgecolor="black",
    linewidth=2
)

# Ramsey highlighted
gdf_ramsey.plot(
    ax=ax2,
    facecolor="#b02a2a",
    edgecolor="black",
    linewidth=2.4
)

# Label Ramsey
ramsey_pt = gdf_ramsey.geometry.representative_point().iloc[0]
ax2.text(
    ramsey_pt.x,
    ramsey_pt.y,
    "Ramsey",
    color="white",
    fontsize=18,
    weight="bold",
    ha="center",
    va="center"
)

# Zoom to TCMA
ax2.set_xlim(tcma_minx, tcma_maxx)
ax2.set_ylim(tcma_miny, tcma_maxy)
ax2.set_axis_off()
ax2.set_aspect("equal")

# Save figure 2 (PNG + SVG)
fig2_png = os.path.join(out_dir, "TCMA_7counties_Ramsey.png")
fig2_svg = os.path.join(out_dir, "TCMA_7counties_Ramsey.svg")
fig2.savefig(fig2_png, dpi=300, bbox_inches="tight")
fig2.savefig(fig2_svg, dpi=300, bbox_inches="tight")
plt.close(fig2)

print("✅ Figures saved to:", out_dir)
print("   -", fig1_png)
print("   -", fig1_svg)
print("   -", fig2_png)
print("   -", fig2_svg)
