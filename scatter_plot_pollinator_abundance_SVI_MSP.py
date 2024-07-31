import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import re
import glob
import os

output_folder = "D:/Shared drives/Urban Workflow/Data/Pollination/Figure/"
input_folder = r"D:\Shared drives\Urban Workflow\Data\Pollination\output\11_cities\MSP"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to add trend line, R-squared, and p-value
def add_trendline(ax, x, y, color):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    ax.plot(x, slope * x + intercept, color=color)
    return r_value**2, p_value

# Process each file in the input folder
for file_path in glob.glob(os.path.join(input_folder, "*.csv")):
    print(file_path)
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Extract city name from the filename after "pollinator_abundance_general_annual_" and before "_zonal"
    city_name_match = re.search(r'pollinator_abundance_general_annual_(\w+)_zonal', file_path)
    city_name = city_name_match.group(1) if city_name_match else "City"
    print(city_name)

    # Calculate population density
    data['pop_density'] = data['E_TOTPOP'] / data['AREA_SQMI']

    # Filter data to only include rows where pop_density > 580 and count > 0
    filtered_data_pov = data[(data['pop_density'] > 580) & (data['count'] > 0) & (data['EP_POV150'] >= 0)]
    filtered_data_min = data[(data['pop_density'] > 580) & (data['count'] > 0) & (data['EP_MINRTY'] >= 0)]

    # Create a figure with two subplots (one for poverty and one for minority)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 12))

    # Create a scatter plot for max pollinator abundance vs EP_POV150 (poverty)
    ax1.scatter(filtered_data_pov['EP_POV150'], filtered_data_pov['max'], alpha=0.5, color='blue', label='Poverty')
    ax1.set_xlabel('% Poverty', fontsize=14)
    ax1.set_ylabel('Maximum Pollinator Abundance', fontsize=14)
    ax1.set_title("Minneapolis – St. Paul", fontsize=16)
    ax1.tick_params(axis='x', labelsize=14)
    ax1.tick_params(axis='y', labelsize=14)
    r_squared, p_value = add_trendline(ax1, filtered_data_pov['EP_POV150'], filtered_data_pov['max'], color='red')
    p_value_text = "< 0.0001" if p_value < 0.0001 else f"{p_value:.4f}"
    ax1.legend([f'R²={r_squared:.2f}, p={p_value_text}'], fontsize=14)

    # Create a scatter plot for max pollinator abundance vs EP_MINRTY (minority)
    ax2.scatter(filtered_data_min['EP_MINRTY'], filtered_data_min['max'], alpha=0.5, color='lightgreen', label='Minority')
    ax2.set_xlabel('% Minority', fontsize=14)
    ax2.set_ylabel('Maximum Pollinator Abundance', fontsize=14)
    ax2.set_title("Minneapolis – St. Paul", fontsize=16)
    ax2.tick_params(axis='x', labelsize=14)
    ax2.tick_params(axis='y', labelsize=14)
    r_squared, p_value = add_trendline(ax2, filtered_data_min['EP_MINRTY'], filtered_data_min['max'], color='red')
    p_value_text = "< 0.0001" if p_value < 0.0001 else f"{p_value:.4f}"
    ax2.legend([f'R²={r_squared:.2f}, p={p_value_text}'], fontsize=14)

    # Save the figure
    file_name = os.path.join(output_folder, f'{city_name}_pollinator_abundance.png')
    fig.tight_layout(pad=3.0)
    fig.savefig(file_name, dpi=300)

    # Show the figure
    plt.show()
