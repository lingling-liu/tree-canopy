from osgeo import gdal 
import os
from pathlib import Path
import pygeoprocessing


# directory = "D:/Shared drives/Urban Workflow/UCM TCMA/Existing_Data/resize/"
# output = "D:/Shared drives/Urban Workflow/UCM TCMA/Existing_Data/resize/reproject/"

directory =  "D:/Shared drives/Urban Workflow/Minneapolis/New_NLCD/New_air_temperature/"
output = "D:/Shared drives/Urban Workflow/Minneapolis/New_NLCD/New_air_temperature/reproject/"

ref = "D:/Shared drives/Urban Workflow/Minneapolis/New_NLCD/New_air_temperature/T_air_Joe_01.tif"

#vector_mask = "D:/My Drive/World Bank/Ethiopia/SWY/input_data_Water_Yield/admin_boundary/eth_admbnda_adm0_buffer_50km.shp"
ref_info = pygeoprocessing.get_raster_info(ref)
pixel_size  = ref_info['pixel_size']
bounding_box = ref_info['bounding_box']
print(bounding_box)
print(pixel_size)
projection_wkt = ref_info['projection_wkt']


for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f): 
        filename = Path(f).stem
        src = f
        dest = output + filename+"_reproject.tif"
        print(dest)
        print(src)
        pygeoprocessing.geoprocessing.align_and_resize_raster_stack([src], [dest],['near'],pixel_size,bounding_box,target_projection_wkt=projection_wkt)
                                                                    #vector_mask_options={"mask_vector_path": vector_mask})