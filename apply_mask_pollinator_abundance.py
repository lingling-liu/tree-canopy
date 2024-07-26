import geopandas as gpd
import rasterio
import rasterio.mask
import os
import numpy as np
from shapely.geometry import mapping
import glob

# Define the raster folder and shapefile directory
raster_folder = r'D:\Shared drives\Urban Workflow\Data\Pollination\INVEST\6_cities'
land_cover_folder = r"D:\Shared drives\Urban Workflow\Data\Pollination\added-6-cities\Land_cover\reproject"

# Get all .tif files using glob
files = glob.glob(os.path.join(raster_folder, '*.tif'))
land_cover_files = glob.glob(os.path.join(land_cover_folder, '*.tif'))

# Print the list of .tif files
for tif_file in files:
    print(tif_file)

shapefile_dir = r"D:\Shared drives\Urban Workflow\Data\Pollination\Selected_Cities"

output_raster_dir = os.path.join(raster_folder, "Masked")
os.makedirs(output_raster_dir, exist_ok=True)

# List of cities to filter
cities = {
    "Boston": "Boston",
    "Baltimore": "Baltimore",
    "Miami": "Miami_FL",
    "Phoenix": "Phoenix",
    "Los Angeles": "Los_Angeles",
    "San Francisco": "San_Francisco"
}

# List of land cover types to mask
land_cover_types_to_mask = [0, 11, 111, 112, 113, 12, 121, 122, 123, -10000]

processed_cities = set()

for file in files:
    if file.endswith(".tif"):
        # Identify the city from the raster filename
        city = None
        for c in cities:
            if c.replace(' ', '_').lower() in file.lower():
                city = c
                break
        
        if city and cities[city] not in processed_cities:
            city_shapefile = os.path.join(shapefile_dir, f"{cities[city]}.shp")
            if os.path.exists(city_shapefile):
                city_gdf = gpd.read_file(city_shapefile)
                with rasterio.open(file) as src:
                    # Reproject the shapefile to match the raster CRS
                    city_gdf = city_gdf.to_crs(src.crs)
                    
                    # Apply mask from shapefile
                    out_image, out_transform = rasterio.mask.mask(src, [mapping(geom) for geom in city_gdf.geometry], crop=True, nodata=-9999)
                    out_meta = src.meta.copy()
                    out_meta.update({
                        "driver": "GTiff",
                        "height": out_image.shape[1],
                        "width": out_image.shape[2],
                        "transform": out_transform,
                        "nodata": -9999
                    })
                    
                    # Find the corresponding land cover raster for the city
                    land_cover_raster = None
                    for lc_file in land_cover_files:
                        if city.replace(' ', '_').lower() in lc_file.lower():
                            land_cover_raster = lc_file
                            break
                    
                    if land_cover_raster:
                        print(city)
                        print(file)
                        print(city_shapefile)
                        print(land_cover_raster)
                        # Open the land cover raster and apply the mask
                        with rasterio.open(land_cover_raster) as lc_src:
                            lc_image, lc_transform = rasterio.mask.mask(lc_src, [mapping(geom) for geom in city_gdf.geometry], crop=True, nodata=-9999)
                            lc_nodata = -10000
                        
                        # Ensure the shapes match
                        if out_image.shape == lc_image.shape:
                            # Mask land cover types and nodata in the raster
                            mask_condition = (np.isin(lc_image, land_cover_types_to_mask))
                            if lc_nodata is not None:
                                mask_condition |= (lc_image == lc_nodata)
                            out_image[mask_condition] = -9999
                            
                            output_filename = os.path.basename(file).replace(".tif", "_masked.tif")
                            output_raster_path = os.path.join(output_raster_dir, output_filename)
                                                        
                            # Check if the output file already exists and delete it
                            if os.path.exists(output_raster_path):
                                os.remove(output_raster_path)
                            
                            with rasterio.open(output_raster_path, "w", **out_meta) as dest:
                                dest.write(out_image)
                        
                            print(f"Masked raster for {city} saved at {output_raster_path}")
                            processed_cities.add(cities[city])
                        else:
                            print(f"Shape mismatch between the raster and land cover for {city}")
                    else:
                        print(f"Land cover raster for {city} does not exist.")
            else:
                print(f"Shapefile for {city} does not exist.")
        else:
            print(f"No corresponding city found for raster {file}")

print("Processing completed.")
