import rasterio
import geopandas as gpd
from rasterstats import zonal_stats
import pandas as pd
import os
import numpy as np

# Define the base folders
raster_folder = r'D:\Shared drives\Urban Workflow\Data\Pollination\INVEST\6_cities\Masked'
shapefile_base_folder = r'D:\Shared drives\Urban Workflow\Data\Pollination\SVI'
output_folder = r'D:\Shared drives\Urban Workflow\Data\Pollination\output'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# List all raster files in the folder
raster_files = [os.path.join(raster_folder, f) for f in os.listdir(raster_folder) if f.endswith('.tif')]

# Define a dictionary to map city names to state names
city_to_state = {
    'Baltimore': 'Maryland',
    'Boston': 'Massachusetts',
    'Miami': 'Florida',
    'Phoenix': 'Arizona',
    'Los_Angeles': 'California',
    'San_Francisco': 'California',
}

# List of cities
cities = ["Boston", "Baltimore", "Miami", "Phoenix", "Los_Angeles", "San_Francisco"]

# Function to extract the city name from the raster file name
def extract_city_name(raster_filename):
    parts = raster_filename.split('_')
    if parts[-2] in ['Los', 'San']:
        return '_'.join(parts[-2:])
    else:
        return parts[-1]  # Assuming the city name is the last part

# Loop through each raster file
for raster_file in raster_files:
    print('          ')
    # Open the raster file
    with rasterio.open(raster_file) as src:
        raster_data = src.read(1)
        affine = src.transform
        raster_crs = src.crs

        # Extract the base name of the raster file
        raster_base = os.path.basename(raster_file).replace('.tif', '')

        # Extract the city name
        city_name = extract_city_name(raster_base)
        
        # Get the corresponding state name from the city_to_state dictionary
        state_name = city_to_state.get(city_name)
        
        if state_name is not None:
            # Define the path to the corresponding shapefile
            shapefile_path = os.path.join(shapefile_base_folder, state_name, f'SVI2022_{state_name.upper()}_tract.gdb')
            print(raster_base)
            print(shapefile_path)
            # Check if the shapefile exists
            if os.path.exists(shapefile_path):
                # Open the shapefile
                shapefile = gpd.read_file(shapefile_path)

                # Reproject the shapefile to match the raster CRS if necessary
                if shapefile.crs != raster_crs:
                    shapefile = shapefile.to_crs(raster_crs)
                
                # Mask raster data to only include values >= 0
                mask = raster_data >= 0
                masked_raster_data = np.where(mask, raster_data, np.nan)
                print(np.nanmax(masked_raster_data))

                # Perform zonal statistics
                stats = zonal_stats(shapefile, masked_raster_data, affine=affine, stats=['mean', 'min', 'max', 'sum', 'count'])

                # Add the results to a DataFrame
                df_stats = pd.DataFrame(stats)

                # Concatenate the shapefile DataFrame with the stats DataFrame
                df_combined = pd.concat([shapefile.reset_index(drop=True), df_stats], axis=1)

                # Define the output CSV file path
                output_csv_path = os.path.join(output_folder, f"{raster_base}_zonal_stats.csv")

                # Save the results to a CSV file
                df_combined.to_csv(output_csv_path, index=False)

                print(f"Zonal statistics saved to {output_csv_path}")
            else:
                print(f"Shapefile for {state_name} not found.")
        else:
            print(f"State name could not be determined for city {city_name} in raster file {raster_base}.")
