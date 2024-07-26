import os
import glob
import rasterio
import numpy as np

# Define the folders
raster_folder = r'D:\Shared drives\Urban Workflow\Data\Pollination\INVEST\Earlier_6_cities'
land_cover_folder = r"D:\Shared drives\Urban Workflow\Data\Pollination\new_NLCD\reproject_linear"

# Get all .tif files
main_raster_files = glob.glob(os.path.join(raster_folder, '*.tif'))
land_cover_files = glob.glob(os.path.join(land_cover_folder, '*.tif'))

# Create output directory for masked rasters
output_raster_dir = os.path.join(raster_folder, "Masked")
os.makedirs(output_raster_dir, exist_ok=True)

# Dictionary mapping cities to their file identifiers
cities = {
    "Denver": "Denver",
    "NY": "New_York",
    "SA": "San_Antonio",
    "SF": "San_Francisco",
    "TCMA": "TCMA",
    "Chicago": "Chicago"
}

# Land cover types to mask
land_cover_types_to_mask = [0, 11, 111, 112, 113, 12, 121, 122, 123]

# Loop through each city
for city, city_name in cities.items():
    # Find corresponding files
    print('             ')
    main_raster_file = next((f for f in main_raster_files if city_name in f), None)
    land_cover_file = next((f for f in land_cover_files if city in f), None)
    print(main_raster_file)
    print(land_cover_file)

    if main_raster_file and land_cover_file:
        # Open the land cover raster
        with rasterio.open(land_cover_file) as land_cover_src:
            land_cover = land_cover_src.read(1)
            land_cover_meta = land_cover_src.meta

        # Open the main raster
        with rasterio.open(main_raster_file) as main_raster_src:
            main_raster = main_raster_src.read(1)
            main_raster_meta = main_raster_src.meta

        # Apply the mask
        mask = np.isin(land_cover, land_cover_types_to_mask)
        nodata_value = main_raster_meta.get('nodata', -9999)  # Set to a default non-data value if not specified
        main_raster[mask] = nodata_value

        # Update the metadata for the output raster
        main_raster_meta.update(dtype=rasterio.float32)

        # Define the output path
        output_raster_file = os.path.join(output_raster_dir, f'masked_{os.path.basename(main_raster_file)}')

        # Write the masked raster to a new file
        with rasterio.open(output_raster_file, 'w', **main_raster_meta) as dst:
            dst.write(main_raster.astype(rasterio.float32), 1)

        print(f'Masked raster saved to {output_raster_file}')
    else:
        print(f'Missing files for city: {city}')
