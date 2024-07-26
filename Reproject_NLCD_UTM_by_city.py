import os
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from pyproj import CRS

# Function to determine UTM zone EPSG code
def get_utm_crs(lat, lon):
    zone_number = int((lon + 180) / 6) + 1
    if lat >= 0:
        epsg_code = 32600 + zone_number
    else:
        epsg_code = 32700 + zone_number
    return CRS.from_epsg(epsg_code)

# Reproject raster to UTM and set zero values to NoData
def reproject_to_utm(input_raster_path, output_raster_path, utm_crs):
    with rasterio.open(input_raster_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, utm_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': utm_crs,
            'transform': transform,
            'width': width,
            'height': height,
            'nodata': 0
        })

        # Create an in-memory array for the reprojected data
        reprojected_array = np.empty((src.count, height, width), dtype=src.dtypes[0])

        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=reprojected_array[i-1],
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=utm_crs,
                resampling=Resampling.nearest,
                dst_nodata=0
            )

        # Set zeros to NoData in the reprojected array
        reprojected_array[reprojected_array == 0] = kwargs['nodata']

        # Write the reprojected array to the output file
        with rasterio.open(output_raster_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                dst.write(reprojected_array[i-1], i)

# Coordinates of cities (latitude, longitude)
cities_coords = {
    'Boston': (42.3601, -71.0589),
    'Baltimore': (39.2904, -76.6122),
    'Miami': (25.7617, -80.1918),
    'Phoenix': (33.4484, -112.0740),
    'Los Angeles': (34.0522, -118.2437),
    'San Francisco': (37.7749, -122.4194)
}

# Path to the folder containing raster files
input_folder = r"D:\Shared drives\Urban Workflow\Data\Pollination\added-6-cities\Land_cover"
output_folder = r"D:\Shared drives\Urban Workflow\Data\Pollination\added-6-cities\Land_cover\reproject"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".tif"):
        input_raster_path = os.path.join(input_folder, filename)
        
        # Determine which city the file belongs to
        for city, coords in cities_coords.items():
            if city.replace(' ', '_') in filename:
                lat, lon = coords
                utm_crs = get_utm_crs(lat, lon)
                
                # Change output file extension to _UTM.tif
                base_filename = os.path.splitext(filename)[0]
                output_raster_path = os.path.join(output_folder, f"{base_filename}_UTM.tif")
                
                # Reproject the raster file
                reproject_to_utm(input_raster_path, output_raster_path, utm_crs)
                
                print(f"{filename} reprojected to {utm_crs.to_epsg()} for {city}")

print("Processing completed.")
