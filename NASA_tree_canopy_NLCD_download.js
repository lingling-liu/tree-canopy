//NASA_tree_canopy_download


var Tree_cover = ee.ImageCollection("NASA/MEASURES/GFCC/TC/v3");
var SA = ee.FeatureCollection("users/liu02034/SanAntonioTX_Project");
var NLCD = ee.ImageCollection("USGS/NLCD_RELEASES/2019_REL/NLCD");

var batch = require('users/fitoprincipe/geetools:batch');
var region = SA;

/*Map.addLayer(Tanu, {}, 'Tanu', false); 
Map.addLayer(Joe, {}, 'Joe', false); */

Map.addLayer(SA, {}, 'SA', false);

var GDriveOutputImgFolder = 'GEEOutputs'; 

//tree canopy
var FirstYear = 2015;
var LastYear = 2015;
var SelectedVariableName = 'tree_canopy_cover'; 
var coll1 =  Tree_cover.filterDate(String(FirstYear)+'-01-01', String(LastYear)+'-12-31').filterBounds(region).select([SelectedVariableName]); 
print("ori",coll1);   
//Map.addLayer(coll1, {}, 'tree_cover', false); 

var mosaic = coll1.mosaic();
Map.addLayer(mosaic, {}, 'mosaic', false); 
print("mosaic",mosaic); 

//NLCD 2016
var FirstYear = 2016;
var LastYear = 2016;
var SelectedVariableName = 'landcover'; 
var coll1_NLCD =  NLCD.filterDate(String(FirstYear)+'-01-01', String(LastYear)+'-12-31').filterBounds(region).select([SelectedVariableName]); 
print("ori_NLCD",coll1_NLCD);   

var mosaic_NLCD = coll1_NLCD.mosaic();
Map.addLayer(mosaic_NLCD, {}, 'mosaic_NLCD', false); 
print("mosaic_NLCD",mosaic_NLCD); 


Export.image.toDrive({
      image: mosaic,
      description: 'Tree_canopy_NASA_30m_SA',
      scale: 30,
      region: region,
      maxPixels: 1.0e13,
      folder: GDriveOutputImgFolder,
    });
    
Export.image.toDrive({
      image: mosaic_NLCD,
      description: 'NLCD_2016_30m_SA',
      scale: 30,
      region: region,
      maxPixels: 1.0e13,
      folder: GDriveOutputImgFolder,
    });