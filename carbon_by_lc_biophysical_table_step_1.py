import os
import pygeoprocessing

# Change the current working directory
new_directory = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\RS parameterization\biomass_SA"
os.chdir(new_directory)

# Define the LULC file path
lulc_file = r"D:\Shared drives\Urban Workflow\Data\Urban_LTER\RS parameterization\lulc_overlay_3857.tif"

# List all .tif files in the new_directory
biomass_sa_files = [f for f in os.listdir(new_directory) if f.endswith('.tif')]

# Get the full path for the biomass files
biomass_sa_files = [os.path.join(new_directory, f) for f in biomass_sa_files]

# Get the raster info from the LULC file
info = pygeoprocessing.get_raster_info(lulc_file)
target_pixel_size = info['pixel_size']

# Prepare the output file paths
aligned_files = [f"aligned_{os.path.splitext(os.path.basename(f))[0]}.tif" for f in biomass_sa_files]
print(aligned_files)

# Align and resize the biomass raster stack to the LULC file
pygeoprocessing.align_and_resize_raster_stack(
    biomass_sa_files + [lulc_file],
    aligned_files + ['aligned_lulc.tif'],
    ['near'] * len(biomass_sa_files + [lulc_file]),
    target_pixel_size,
    'intersection',
)

print("Alignment and resizing completed.")
