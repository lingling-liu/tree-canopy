pro tree_canopy_reclassify_NASA_SA
  
  ; Read NASA 30 m data
  infile = "Y:\people\liu02034\Tree_canopy\SA\Tree_canopy_NASA_30m_SA_new.tif"
  data_tree1 = READ_TIFF(infile,geotiff = geotiff_tree) ; 255 filled value 
  data_tree = data_tree1/100.0 ; make sure scale is same 
  
  nlcd_id = [12,21,22,23,24,31,41,42,43,51,52,71,72,73,74,81,82,90,95]
  print,n_elements(nlcd_id)
  nlcd_name = ["Perennial Ice/Snow","Developed, Open Space","Developed, Low Intensity","  Developed, Medium Intensity","Developed High Intensity",$
    " Barren Land","Deciduous Forest","Evergreen Forest","Mixed Forest","Dwarf Scrub","Shrub_Scrub","Grassland_Herbaceous","Sedge_Herbaceous","Lichens","Moss",$
    "Pasture_Hay","Cultivated Crops","Woody Wetlands"," Emergent Herbaceous Wetlands"]

  ;read clipped NLCD data
  infile = "Y:\people\liu02034\Tree_canopy\SA\NLCD_2016_30m_SA_new.tif"
  data_nlcd = READ_TIFF(infile,geotiff = geotiff_nlcd) ; 255 filled value 

  array = data_nlcd
  nlcd_classes = array[UNIQ(array, SORT(array))]
  print, nlcd_classes

  result =  fix(data_nlcd)
  index = where(result eq 255)
  result[index] = 0

  for i=0,n_elements(nlcd_classes)-2 do begin ; exclude 255
    print, nlcd_classes[i]
    index = where(nlcd_id eq nlcd_classes[i], count)
    ; exclude forest types
    if nlcd_classes[i] ne 41 and nlcd_classes[i] ne 42 and nlcd_classes[i] ne 43 then begin 
      if count eq 1 then begin
        index1 = where(data_tree ne 2.55 and data_nlcd eq nlcd_classes[i],count1)
        if count1 gt 100 then begin
          index11 = where(data_tree le 0.07 and data_nlcd eq nlcd_classes[i],count11)
          if count11 gt 0 then result[index11] = nlcd_classes[i] *10+1
          index22 = where(data_tree gt 0.07 and data_tree le 0.2 and data_nlcd eq nlcd_classes[i],count22)
          if count22 gt 0 then result[index22] = nlcd_classes[i] *10+2
          index33 = where(data_tree gt 0.2 and data_tree le 1 and data_nlcd eq nlcd_classes[i],count33)
          if count33 gt 0 then result[index33] = nlcd_classes[i]*10+3
        endif
      endif
    endif
  endfor
  
 ;0 is invalid value
  path = "Y:\people\liu02034\Tree_canopy\30m\NLCD_2016_Land_Cover_new_addingtree_NASA_SA.tif"
  WRITE_TIFF,path,result,COMPRESSION=1, GEOTIFF=geotiff_tree,/short

end