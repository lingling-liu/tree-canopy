import ee
import geemap

ee.Authenticate()
# initialize earth engine api access (required on every run)
ee.Initialize()
Map = geemap.Map()

Tree_cover = ee.ImageCollection("NASA/MEASURES/GFCC/TC/v3")
SA = ee.FeatureCollection("users/liu02034/SanAntonioTX_Project")
NLCD = ee.ImageCollection("USGS/NLCD_RELEASES/2019_REL/NLCD")

region = SA

Map.addLayer(SA, {}, 'SA', False)

GDriveOutputImgFolder = 'GEEOutputs'

#tree canopy
FirstYear = "2015"
LastYear = "2015"
SelectedVariableName = 'tree_canopy_cover'
coll1 =  Tree_cover.filterDate(FirstYear+'-01-01', LastYear+'-12-31').filterBounds(region).select([SelectedVariableName])

print("ori",coll1)
#Map.addLayer(coll1, {}, 'tree_cover', False)

mosaic = coll1.mosaic()
Map.addLayer(mosaic, {}, 'mosaic', False)
print("mosaic",mosaic)

#NLCD 2016
FirstYear = "2016"
LastYear = "2016"
SelectedVariableName = 'landcover'
coll1_NLCD =  NLCD.filterDate(FirstYear+'-01-01', LastYear+'-12-31').filterBounds(region).select([SelectedVariableName])
print("ori_NLCD",coll1_NLCD)

mosaic_NLCD = coll1_NLCD.mosaic()
Map.addLayer(mosaic_NLCD, {}, 'mosaic_NLCD', False)
print("mosaic_NLCD",mosaic_NLCD)

scale = 30;
maxPixels = 1.0e13

task = ee.batch.Export.image.toDrive(
        mosaic,
        description='Tree_canopy_NASA_30m_SA',
        folder=GDriveOutputImgFolder,
        region=region.geometry(),
        scale=scale,
        maxPixels=maxPixels,
    )

task.start()

task = ee.batch.Export.image.toDrive(
        mosaic_NLCD,
        description='NLCD_2016_30m_SA',
        folder=GDriveOutputImgFolder,
        region=region.geometry(),
        scale=scale,
        maxPixels=maxPixels,
    )

task.start()

Map