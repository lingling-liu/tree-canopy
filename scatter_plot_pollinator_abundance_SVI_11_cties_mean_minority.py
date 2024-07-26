import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import re
import glob
import os

output_folder = "D:/Shared drives/Urban Workflow/Data/Pollination/Figure/"
input_folder = "D:/Shared drives/Urban Workflow/Data/Pollination/output/11_cities"

# Function to add trend line, R-squared, and p-value
def add_trendline(ax, x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    ax.plot(x, slope*x + intercept, color='red')
    return r_value**2, p_value

# List to keep track of processed cities for combined plot
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

    # Filter data to only include rows where pop_density > 116 and count > 0
    filtered_data = data[(data['pop_density'] > 116) & (data['count'] > 0) & (data['EP_POV150'] >= 0) & (data['EP_MINRTY'] >= 0)]

    # Create a scatter plot for mean pollinator abundance vs EP_MINRTY
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(filtered_data['EP_MINRTY'], filtered_data['mean'], alpha=0.5, label='Cities')
    ax.set_xlabel('EP_MINRTY', fontsize=14)
    ax.set_ylabel('Mean Pollinator Abundance', fontsize=12)
    ax.set_title(f'{city_name}', fontsize=14)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    r_squared, p_value = add_trendline(ax, filtered_data['EP_MINRTY'], filtered_data['mean'])
    ax.legend([f'R²={r_squared:.2f}, p={p_value:.2f}'], fontsize=14)
    plt.close(fig)

    # Append the plot to the list of city plots
    city_plots.append((city_name, fig))

# Create a combined figure with 3 rows and 4 columns
fig, axs = plt.subplots(3, 4, figsize=(20, 15))
axs = axs.flatten()

for i, (city_name, city_fig) in enumerate(city_plots):
    # Extract the scatter plot from the city figure
    city_ax = city_fig.get_axes()[0]
    city_ax.figure.canvas.draw()
    width, height = city_ax.figure.get_size_inches() * city_ax.figure.dpi
    width = int(width)
    height = int(height)
    img = np.frombuffer(city_ax.figure.canvas.tostring_rgb(), dtype='uint8').reshape(height, width, 3)

    # Display the city scatter plot in the combined figure
    axs[i].imshow(img)
    axs[i].axis('off')  # Hide the axes
    #axs[i].text(0.5, -0.1, city_name, ha='center', va='center', transform=axs[i].transAxes, fontsize=12)

# Remove the last empty subplot if there are less than 12 cities
if len(city_plots) < 12:
    for j in range(len(city_plots), 12):
        fig.delaxes(axs[j])

# Adjust the layout to make the spacing between subplots tighter
plt.subplots_adjust(wspace=0, hspace=0)

# Save the combined figure as an image file
combined_file_name = os.path.join(output_folder, "combined_mean_pollinator_EP_MINRTY.png")
fig.tight_layout(pad=2.0)
fig.savefig(combined_file_name)
plt.show()
