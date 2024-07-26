import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import re
import glob
import os

output_folder = "D:/Shared drives/Urban Workflow/Data/Pollination/Figure/"
input_folder = "D:/Shared drives/Urban Workflow/Data/Pollination/output/Earlier_6_cities/"

# Function to add trend line, R-squared, and p-value
def add_trendline(ax, x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    ax.plot(x, slope*x + intercept, color='red')
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
    filtered_data = data[(data['pop_density'] > 580) & (data['count'] > 0) & (data['EP_POV150'] >= 0) & (data['EP_MINRTY'] >= 0)]

    # Filter data to only include rows where pop_density > 116 and count > 0
    filtered_data1 = data[(data['pop_density'] > 116) & (data['count'] > 0) & (data['EP_POV150'] >= 0) & (data['EP_MINRTY'] >= 0)]

    # Create scatter plots in a 2x2 format for mean
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))

    # Cities: Scatter plot EP_POV150 vs. mean
    axs[0, 0].scatter(filtered_data['EP_POV150'], filtered_data['mean'], alpha=0.5, label='Cities')
    axs[0, 0].set_xlabel('EP_POV150')
    axs[0, 0].set_ylabel('Mean Pollinator Abundance')
    axs[0, 0].set_title(f'Cities: {city_name}')
    r_squared, p_value = add_trendline(axs[0, 0], filtered_data['EP_POV150'], filtered_data['mean'])
    axs[0, 0].legend([f'R²={r_squared:.2f}, p={p_value:.2f}'])

    # Cities: Scatter plot EP_MINRTY vs. mean
    axs[0, 1].scatter(filtered_data['EP_MINRTY'], filtered_data['mean'], alpha=0.5, label='Cities')
    axs[0, 1].set_xlabel('EP_MINRTY')
    axs[0, 1].set_ylabel('Mean Pollinator Abundance')
    axs[0, 1].set_title(f'Cities: {city_name}')
    r_squared, p_value = add_trendline(axs[0, 1], filtered_data['EP_MINRTY'], filtered_data['mean'])
    axs[0, 1].legend([f'R²={r_squared:.2f}, p={p_value:.2f}'])

    # Cities and Towns: Scatter plot EP_POV150 vs. mean
    axs[1, 0].scatter(filtered_data1['EP_POV150'], filtered_data1['mean'], alpha=0.5, label='Cities and Towns')
    axs[1, 0].set_xlabel('EP_POV150')
    axs[1, 0].set_ylabel('Mean Pollinator Abundance')
    axs[1, 0].set_title(f'Cities and Towns: {city_name}')
    r_squared, p_value = add_trendline(axs[1, 0], filtered_data1['EP_POV150'], filtered_data1['mean'])
    axs[1, 0].legend([f'R²={r_squared:.2f}, p={p_value:.2f}'])

    # Cities and Towns: Scatter plot EP_MINRTY vs. mean
    axs[1, 1].scatter(filtered_data1['EP_MINRTY'], filtered_data1['mean'], alpha=0.5, label='Cities and Towns')
    axs[1, 1].set_xlabel('EP_MINRTY')
    axs[1, 1].set_ylabel('Mean Pollinator Abundance')
    axs[1, 1].set_title(f'Cities and Towns: {city_name}')
    r_squared, p_value = add_trendline(axs[1, 1], filtered_data1['EP_MINRTY'], filtered_data1['mean'])
    axs[1, 1].legend([f'R²={r_squared:.2f}, p={p_value:.2f}'])

    # Save the plot as an image file
    file_name_mean = output_folder + f"{city_name}_mean_pollinator_SVI.png"
    plt.savefig(file_name_mean)

    # plt.tight_layout()
    # plt.show()

    # Create scatter plots in a 2x2 format for max
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))

    # Cities: Scatter plot EP_POV150 vs. max
    axs[0, 0].scatter(filtered_data['EP_POV150'], filtered_data['max'], alpha=0.5, label='Cities')
    axs[0, 0].set_xlabel('EP_POV150')
    axs[0, 0].set_ylabel('Max Pollinator Abundance')
    axs[0, 0].set_title(f'Cities: {city_name}')
    r_squared, p_value = add_trendline(axs[0, 0], filtered_data['EP_POV150'], filtered_data['max'])
    axs[0, 0].legend([f'R²={r_squared:.2f}, p={p_value:.2f}'])

    # Cities: Scatter plot EP_MINRTY vs. max
    axs[0, 1].scatter(filtered_data['EP_MINRTY'], filtered_data['max'], alpha=0.5, label='Cities')
    axs[0, 1].set_xlabel('EP_MINRTY')
    axs[0, 1].set_ylabel('Max Pollinator Abundance')
    axs[0, 1].set_title(f'Cities: {city_name}')
    r_squared, p_value = add_trendline(axs[0, 1], filtered_data['EP_MINRTY'], filtered_data['max'])
    axs[0, 1].legend([f'R²={r_squared:.2f}, p={p_value:.2f}'])

    # Cities and Towns: Scatter plot EP_POV150 vs. max
    axs[1, 0].scatter(filtered_data1['EP_POV150'], filtered_data1['max'], alpha=0.5, label='Cities and Towns')
    axs[1, 0].set_xlabel('EP_POV150')
    axs[1, 0].set_ylabel('Max Pollinator Abundance')
    axs[1, 0].set_title(f'Cities and Towns: {city_name}')
    r_squared, p_value = add_trendline(axs[1, 0], filtered_data1['EP_POV150'], filtered_data1['max'])
    axs[1, 0].legend([f'R²={r_squared:.2f}, p={p_value:.2f}'])

    # Cities and Towns: Scatter plot EP_MINRTY vs. max
    axs[1, 1].scatter(filtered_data1['EP_MINRTY'], filtered_data1['max'], alpha=0.5, label='Cities and Towns')
    axs[1, 1].set_xlabel('EP_MINRTY')
    axs[1, 1].set_ylabel('Max Pollinator Abundance')
    axs[1, 1].set_title(f'Cities and Towns: {city_name}')
    r_squared, p_value = add_trendline(axs[1, 1], filtered_data1['EP_MINRTY'], filtered_data1['max'])
    axs[1, 1].legend([f'R²={r_squared:.2f}, p={p_value:.2f}'])

    # Save the plot as an image file
    file_name_max = output_folder + f"{city_name}_max_pollinator_SVI.png"
    plt.savefig(file_name_max)

    # plt.tight_layout()
    # plt.show()
