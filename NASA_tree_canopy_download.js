//NASA_tree_canopy_download


var Tree_cover = ee.ImageCollection("NASA/MEASURES/GFCC/TC/v3");
var SA = ee.FeatureCollection("users/liu02034/SanAntonioTX_Project");


var batch = require('users/fitoprincipe/geetools:batch');
var region = SA;

Map.addLayer(SA, {}, 'SA', false);

var GDriveOutputImgFolder = 'GEEOutputs'; 

var FirstYear = 2015;
var LastYear = 2015;

var SelectedVariableName = 'tree_canopy_cover'; 
var coll1 =  Tree_cover.filterDate(String(FirstYear)+'-01-01', String(LastYear)+'-12-31').filterBounds(region).select([SelectedVariableName]); 
print("ori",coll1);   
Map.addLayer(coll1, {}, 'tree_cover', false); 

var mosaic = coll1.mosaic();
Map.addLayer(mosaic, {}, 'mosaic', false); 
print("mosaic",mosaic); 

Export.image.toDrive({
      image: mosaic,
      description: 'Tree_canopy_NASA_30m_SA',
      scale: 30,
      region: region,
      maxPixels: 1.0e13,
      folder: GDriveOutputImgFolder,
    });