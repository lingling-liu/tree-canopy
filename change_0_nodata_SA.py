from osgeo import gdal 
import os
from pathlib import Path

directory = "C:/tree_canopy/SA/data/reclassify"

translateoptions = gdal.TranslateOptions(gdal.ParseCommandLine("-a_nodata 0 COMPRESS=LZW"))

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f): 
        filename = Path(f).stem
        src = f
        dest = "C:/tree_canopy/SA/data/reclassify/nodata/"+ filename+"_nodata0_compressed.tif"
        print(dest)
        print(src)
        ds = gdal.Translate(dest,src,options=translateoptions)