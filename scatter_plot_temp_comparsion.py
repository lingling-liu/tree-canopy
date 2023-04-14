#https://stackoverflow.com/questions/2369492/generate-a-heatmap-using-a-scatter-data-set
import rasterio
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os
from scipy.ndimage.filters import gaussian_filter
import matplotlib.cm as cm

title_list = ['baseline','Tanu','Joe','NASA',]

def myplot(x, y, s, bins=1000):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent


ground_temp = "D:/Shared drives/Urban Workflow/UCM TCMA/Existing_Data/resize/reproject/JJA_Day_Temp1_resize_reproject.tif"
# model_temp = "D:/Shared drives/Urban Workflow/Minneapolis/New_NLCD/New_air_temperature/T_air_baseline.tif"

# model_temp = "D:/Shared drives/Urban Workflow/Minneapolis/New_NLCD/New_air_temperature/T_air_Joe_01.tif"

directory =  "D:/Shared drives/Urban Workflow/Minneapolis/New_NLCD/New_air_temperature/reproject/"

# create a figure with two subplots
fig, ax = plt.subplots(1, 4, figsize=(20,5))
i=0

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    print(f)
    # checking if it is a file
    if os.path.isfile(f): 
    # Load the two rasters
        print(f)
        with rasterio.open(ground_temp) as src1, rasterio.open(f) as src2:
            # Read the data into arrays
            data1 = src1.read(1).flatten()
            data2 = src2.read(1).flatten()

        print(min(data1), max(data1))
        print(len(data1))
        print(type(data1))

        print(min(data2), max(data2))
        print(len(data2))

        # define the range
        lower = 20
        upper = 30

        data1_filtered = data1[(data1 >= lower) & (data1 <= upper) & (data2 >= lower) & (data2 <= upper)]
        data2_filtered = data2[(data1 >= lower) & (data1 <= upper) & (data2 >= lower) & (data2 <= upper)]
        print(len(data1_filtered))
        print(min(data1_filtered), max(data1_filtered))

        print(len(data2_filtered))
        print(min(data2_filtered), max(data2_filtered))

        x = data1_filtered
        y = data2_filtered

        #s= 16
        #img, extent = myplot(x, y, s)
        #ax[i].imshow(img, extent=extent, origin='lower', cmap=cm.jet)

        ax[i].scatter(data1_filtered, data2_filtered, alpha=0.5, marker='.')

        # calculate the regression line
        coeffs = np.polyfit(x, y, 1)
        line = np.poly1d(coeffs)

        #line_x = np.array([0, 1])
        #line_y = coeffs[0]*line_x + coeffs[1]

        # add the regression line
        ax[i].plot(x, line(x), color='red')

        # calculate the linear regression parameters
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        # add text with the R2 and P-value
        textstr = '\n'.join((
            r'$R^2=%.2f$' % (r_value**2,),
            r'$P=%.2f$' % (p_value,)))
        ax[i].text(25, 23.5, textstr, fontsize=14, verticalalignment='top')

        ax[i].set_xlabel('Ground Day temp')
        ax[i].set_ylabel(title_list[i])

        # set the x and y axis ranges
        # ax[i].set_xlim(24, 25.6)
        # ax[i].set_ylim(23, 25)
        
        i = i+1

# adjust the layout
plt.tight_layout()
# plt.show()

#fig.suptitle('Preciptation',fontname='Arial', fontsize=20, fontweight='bold')
#plt.show()
os.chdir('D:\My Drive\Tree_Canopy\Fig')
plt.savefig("scatter_plot_ground_day_modelled.png",dpi =300)