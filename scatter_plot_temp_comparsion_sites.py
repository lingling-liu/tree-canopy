#https://stackoverflow.com/questions/2369492/generate-a-heatmap-using-a-scatter-data-set
import rasterio
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os
from scipy.ndimage.filters import gaussian_filter
import matplotlib.cm as cm
import pandas as pd

title_list = ['baseline','Tanu','Joe','NASA',]

def myplot(x, y, s, bins=1000):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent

# Set path to the Excel file and sheet name
file_path = "D:/Shared drives/Urban Workflow/UCM TCMA/Existing_Data/Twine_UHI_2016/ground_modelled_sites_temperture.xlsx"
sheet_name = 'Sheet1'
# Read the Excel file into a Pandas DataFrame
df = pd.read_excel(file_path, sheet_name=sheet_name)

# create a figure with two subplots
fig, ax = plt.subplots(1, 4, figsize=(20,5))
i=0

#****************************ground vs baseline********************************************

data1 = df["JJA_Day_Te"]
data2 = df['T_air_base']

# define the range
lower = 15
upper = 35

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
#ax[i].plot(x, line(x), color='red')
ax[i].plot([22,32], [22,32], color='red',linestyle='--')

# calculate the linear regression parameters
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# add text with the R2 and P-value
textstr = '\n'.join((
r'$R^2=%.3f$' % (r_value**2,),
r'$P=%.3f$' % (p_value,)))
ax[i].text(28, 24, textstr, fontsize=14, verticalalignment='top')

ax[i].set_xlabel('Ground Day temp')
ax[i].set_ylabel(title_list[i])

# set the x and y axis ranges
ax[i].set_xlim(22, 32)
ax[i].set_ylim(22, 32)

i = i+1

#*****************************************ground vs Tanu*************************************
data1 = df["JJA_Day_Te"]
data2 = df['T_air_Tanu']


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
#ax[i].plot(x, line(x), color='red')
ax[i].plot([22,32], [22,32], color='red',linestyle='--')

# calculate the linear regression parameters
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# add text with the R2 and P-value
textstr = '\n'.join((
r'$R^2=%.3f$' % (r_value**2,),
r'$P=%.3f$' % (p_value,)))
ax[i].text(28, 24, textstr, fontsize=14, verticalalignment='top')

ax[i].set_xlabel('Ground Day temp')
ax[i].set_ylabel(title_list[i])

# set the x and y axis ranges
ax[i].set_xlim(22, 32)
ax[i].set_ylim(22, 32)

i = i+1

#*****************************************ground vs Joe************************************* 
data1 = df["JJA_Day_Te"]
data2 = df['T_air_Joe']


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
#ax[i].plot(x, line(x), color='red')
ax[i].plot([22,32], [22,32], color='red',linestyle='--')

# calculate the linear regression parameters
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# add text with the R2 and P-value
textstr = '\n'.join((
r'$R^2=%.3f$' % (r_value**2,),
r'$P=%.3f$' % (p_value,)))
ax[i].text(28, 24, textstr, fontsize=14, verticalalignment='top')

ax[i].set_xlabel('Ground Day temp')
ax[i].set_ylabel(title_list[i])

# set the x and y axis ranges
ax[i].set_xlim(22, 32)
ax[i].set_ylim(22, 32)

i = i+1

#*****************************************ground vs NASA************************************* 
data1 = df["JJA_Day_Te"]
data2 = df['T_air_NASA']


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
#ax[i].plot(x, line(x), color='red')
ax[i].plot([22,32], [22,32], color='red',linestyle='--')

# calculate the linear regression parameters
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# add text with the R2 and P-value
textstr = '\n'.join((
r'$R^2=%.3f$' % (r_value**2,),
r'$P=%.3f$' % (p_value,)))
ax[i].text(28, 24, textstr, fontsize=14, verticalalignment='top')

ax[i].set_xlabel('Ground Day temp')
ax[i].set_ylabel(title_list[i])

# set the x and y axis ranges
ax[i].set_xlim(22, 32)
ax[i].set_ylim(22, 32)

# adjust the layout
plt.tight_layout()
# plt.show()

#fig.suptitle('Preciptation',fontname='Arial', fontsize=20, fontweight='bold')
#plt.show()
os.chdir('D:\My Drive\Tree_Canopy\Fig')
plt.savefig("scatter_plot_ground_day_modelled_sites.png",dpi =300)