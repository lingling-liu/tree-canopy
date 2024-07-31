import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import re
import glob
import os
from matplotlib.ticker import FormatStrFormatter

output_folder = "D:/Shared drives/Urban Workflow/Data/Pollination/Figure/"
input_folder = r"D:\Shared drives\Urban Workflow\Data\Pollination\output\11_cities\10cities"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to add trend line, R-squared, and p-value
def add_trendline(ax, x, y, color):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    ax.plot(x, slope * x + intercept, color=color)
    return r_value**2, p_value

# List to keep track of city plots
city_plots = []

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

    # Create individual figures for each city
    fig_pov, ax1 = plt.subplots(figsize=(6, 6))
    ax1.scatter(filtered_data_pov['EP_POV150'], filtered_data_pov['max'], alpha=0.5, color='blue', label='Poverty')
    ax1.set_xlabel('% Poverty', fontsize=20)
    ax1.set_ylabel('Maximum Pollinator Abundance', fontsize=18)
    ax1.set_title(f'{city_name}', fontsize=22)
    ax1.tick_params(axis='x', labelsize=18)
    ax1.tick_params(axis='y', labelsize=18)
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    r_squared, p_value = add_trendline(ax1, filtered_data_pov['EP_POV150'], filtered_data_pov['max'], color='red')
    p_value_text = "< 0.0001" if p_value < 0.0001 else f"{p_value:.4f}"
    ax1.legend([f'R²={r_squared:.2f}, p={p_value_text}'], fontsize=16)

    fig_min, ax2 = plt.subplots(figsize=(6, 6))
    ax2.scatter(filtered_data_min['EP_MINRTY'], filtered_data_min['max'], alpha=0.5, color='lightgreen', label='Minority')
    ax2.set_xlabel('% Minority', fontsize=20)
    ax2.set_ylabel('Maximum Pollinator Abundance', fontsize=18)
    ax2.set_title(f'{city_name}', fontsize=22)
    ax2.tick_params(axis='x', labelsize=18)
    ax2.tick_params(axis='y', labelsize=18)
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    r_squared, p_value = add_trendline(ax2, filtered_data_min['EP_MINRTY'], filtered_data_min['max'], color='red')
    p_value_text = "< 0.0001" if p_value < 0.0001 else f"{p_value:.4f}"
    ax2.legend([f'R²={r_squared:.2f}, p={p_value_text}'], fontsize=16)

    # Append the individual plots to the city_plots list
    city_plots.append((city_name, fig_pov, fig_min))

# Determine the number of rows needed (3 rows for 6 columns = 18 subplots max)
num_plots = len(city_plots) * 2
num_rows = (num_plots // 6) + (1 if num_plots % 6 != 0 else 0)
num_cols = 6

# Create a combined figure with the appropriate number of rows and columns
fig, axs = plt.subplots(num_rows, num_cols, figsize=(num_cols * 5, num_rows * 5))
axs = axs.flatten()

for i, (city_name, fig_pov, fig_min) in enumerate(city_plots):
    # Extract the scatter plot from the individual figures
    pov_ax = fig_pov.get_axes()[0]
    min_ax = fig_min.get_axes()[0]

    pov_ax.figure.canvas.draw()
    min_ax.figure.canvas.draw()

    pov_width, pov_height = pov_ax.figure.get_size_inches() * pov_ax.figure.dpi
    min_width, min_height = min_ax.figure.get_size_inches() * min_ax.figure.dpi

    pov_width, pov_height = int(pov_width), int(pov_height)
    min_width, min_height = int(min_width), int(min_height)

    pov_img = np.frombuffer(pov_ax.figure.canvas.tostring_rgb(), dtype='uint8').reshape(pov_height, pov_width, 3)
    min_img = np.frombuffer(min_ax.figure.canvas.tostring_rgb(), dtype='uint8').reshape(min_height, min_width, 3)

    # Display the city scatter plot in the combined figure
    axs[2 * i].imshow(pov_img)
    axs[2 * i].axis('off')  # Hide the axes
 
    axs[2 * i + 1].imshow(min_img)
    axs[2 * i + 1].axis('off')  # Hide the axes

      # Add y-axis label for specific subplots
    if city_name in ["San_Francisco", "Chicago", "Miami", "San_Antonio"]:
        axs[2 * i].text(-0.1, 0.5, 'Maximum Pollinator Abundance', va='center', ha='center', rotation='vertical', fontsize=16, transform=axs[2 * i].transAxes)


# Remove the remaining empty subplots
for j in range(2 * i + 2, len(axs)):
    fig.delaxes(axs[j])

# Adjust the layout to make the spacing between subplots tighter
plt.subplots_adjust(wspace=0.1, hspace=0.3)

# Save the combined figure as an image file
combined_file_name = os.path.join(output_folder, "combined_pollinator_abundance_ylabel.png")
fig.tight_layout(pad=3.0)
fig.savefig(combined_file_name, dpi=300)

plt.show()
