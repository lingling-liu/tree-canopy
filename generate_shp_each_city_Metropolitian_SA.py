import geopandas as gpd
import os

# Load the original shapefile
file_path = "C:/Pollination/tl_2019_us_cbsa/tl_2019_us_cbsa.shp"
gdf = gpd.read_file(file_path)

# List of cities to filter
cities = ["Boston", "Baltimore", "Miami", "Phoenix", "Los Angeles", "San Francisco"]

# Output directory
output_dir = "C:/Pollination/Selected_Cities"
os.makedirs(output_dir, exist_ok=True)

# Filter and save each city as a separate shapefile
for city in cities:
    city_gdf = gdf[gdf["NAME"].str.contains(city, case=False)]
    if not city_gdf.empty:
        output_path = os.path.join(output_dir, f"{city.replace(' ', '_')}.shp")
        city_gdf.to_file(output_path, driver='ESRI Shapefile')
        print(f"Shapefile for {city} saved at {output_path}")
    else:
        print(f"No records found for {city}")

print("Processing completed.")
