import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import re
import glob
import os

# Define input and output folders (update these when running locally)
input_folder = "G:/Shared drives/Urban Workflow/Data/Pollination/output/11_cities"
output_folder = "G:/Shared drives/Urban Workflow/Data/Pollination/Figure/"

# Initialize lists for storing data
all_data_poverty = []
all_data_minority = []
city_regression_lines_poverty = []
city_regression_lines_minority = []
csv_files = glob.glob(os.path.join(input_folder, "*.csv"))
print("CSV Files Found:", csv_files)

# Process each file in the input folder
for file_path in csv_files:
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Extract city name from the filename
    city_name_match = re.search(r'pollinator_abundance_general_annual_(\w+)_zonal', file_path)
    city_name = city_name_match.group(1) if city_name_match else "City"

    # Calculate population density
    data['pop_density'] = data['E_TOTPOP'] / data['AREA_SQMI']

    # Filter data to only include relevant rows
    filtered_data = data[(data['pop_density'] > 116) & (data['count'] > 0) & 
                         (data['EP_POV150'] >= 0) & (data['EP_MINRTY'] >= 0)]

    # Append data for composite analysis
    if not filtered_data.empty:
        all_data_poverty.append(filtered_data[['EP_POV150', 'mean']])
        all_data_minority.append(filtered_data[['EP_MINRTY', 'mean']])

    # Calculate regression lines for individual cities
    for x_col, y_col, city_list in [('EP_POV150', 'mean', city_regression_lines_poverty), 
                                     ('EP_MINRTY', 'mean', city_regression_lines_minority)]:
        x = filtered_data[x_col]
        y = filtered_data[y_col]
        if len(x) > 1:  # Ensure there are enough points for regression
            slope, intercept, _, _, _ = stats.linregress(x, y)
            city_list.append((city_name, slope, intercept, x.min(), x.max()))

# Save slopes to a CSV file
slope_data = []
for city_name, slope, _, _, _ in city_regression_lines_poverty:
    slope_data.append([city_name, 'Poverty-Pollinator', slope])
for city_name, slope, _, _, _ in city_regression_lines_minority:
    slope_data.append([city_name, 'Minority-Pollinator', slope])

slope_df = pd.DataFrame(slope_data, columns=['City', 'Relationship', 'Slope'])
slope_df.to_csv(os.path.join(output_folder, "pollinator_abundance_slopes.csv"), index=False)

# Print slopes for poverty-pollinator abundance relationship per city
print("Slopes of Poverty-Pollinator Abundance Relationship by City:")
for city_name, slope, intercept, _, _ in city_regression_lines_poverty:
    print(f"{city_name}: {slope:.4f}")

# Print slopes for minority-pollinator abundance relationship per city
print("Slopes of Minority-Pollinator Abundance Relationship by City:")
for city_name, slope, intercept, _, _ in city_regression_lines_minority:
    print(f"{city_name}: {slope:.4f}")

# Combine data for composite regression analysis
if all_data_poverty:
    combined_poverty = pd.concat(all_data_poverty)
    slope_pov, intercept_pov, _, _, _ = stats.linregress(combined_poverty['EP_POV150'], combined_poverty['mean'])
else:
    combined_poverty = None

if all_data_minority:
    combined_minority = pd.concat(all_data_minority)
    slope_min, intercept_min, _, _, _ = stats.linregress(combined_minority['EP_MINRTY'], combined_minority['mean'])
else:
    combined_minority = None

# Create the figure with two panels
fig, axs = plt.subplots(1, 2, figsize=(14, 6))
y_axis_limits = (-0.05, 0.20)  # Set y-axis limits for both plots

# Left Panel: Pollinator Abundance Index vs. % Poverty
if combined_poverty is not None:
    for city_name, slope, intercept, x_min, x_max in city_regression_lines_poverty:
        x_vals = np.linspace(x_min, x_max, 100)
        axs[0].plot(x_vals, slope * x_vals + intercept, linestyle='dotted', linewidth=1, label=f"{city_name}")

    x_vals = np.linspace(combined_poverty['EP_POV150'].min(), combined_poverty['EP_POV150'].max(), 100)
    axs[0].plot(x_vals, slope_pov * x_vals + intercept_pov, linestyle='solid', linewidth=2, color='black', label="Composite")

axs[0].set_xlabel('% Poverty', fontsize=14)
axs[0].set_ylabel('Pollinator Abundance Index', fontsize=14)
axs[0].set_title('Pollinator Abundance vs. Poverty', fontsize=16)
axs[0].legend(fontsize=10, loc='upper right')
axs[0].set_ylim(y_axis_limits)  # Apply y-axis limits

# Right Panel: Pollinator Abundance Index vs. % Minority
if combined_minority is not None:
    for city_name, slope, intercept, x_min, x_max in city_regression_lines_minority:
        x_vals = np.linspace(x_min, x_max, 100)
        axs[1].plot(x_vals, slope * x_vals + intercept, linestyle='dotted', linewidth=1, label=f"{city_name}")

    x_vals = np.linspace(combined_minority['EP_MINRTY'].min(), combined_minority['EP_MINRTY'].max(), 100)
    axs[1].plot(x_vals, slope_min * x_vals + intercept_min, linestyle='solid', linewidth=2, color='black', label="Composite")

axs[1].set_xlabel('% Minority', fontsize=14)
axs[1].set_ylabel('Pollinator Abundance Index', fontsize=14)
axs[1].set_title('Pollinator Abundance vs. Minority', fontsize=16)
axs[1].legend(fontsize=10, loc='upper right')
axs[1].set_ylim(y_axis_limits)  # Apply y-axis limits

axs[0].tick_params(axis='both', labelsize=14)  # Adjust font size for the left panel
axs[1].tick_params(axis='both', labelsize=14)  # Adjust font size for the right panel

plt.tight_layout()
plt.savefig(os.path.join(output_folder, "pollinator_abundance_analysis_updated_07_31_2025.png"), dpi=300, bbox_inches='tight')
plt.show()
