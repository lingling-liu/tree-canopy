pro tree_canopy_reclassify_joe

  ; read tree canopy percentages
  data_tree = READ_TIFF("/largedisk_a/tree_canopy/original_data/30m/tcma_lc_treecanopy_30m.tif",geotiff = geotiff_tree)
  ns = n_elements(data_tree[*,0])
  nl = n_elements(data_tree[0,*])


  nlcd_id = [12,21,22,23,24,31,41,42,43,51,52,71,72,73,74,81,82,90,95]
  print,n_elements(nlcd_id)
  nlcd_name = ["Perennial Ice/Snow","Developed, Open Space","Developed, Low Intensity","  Developed, Medium Intensity","Developed High Intensity",$
    " Barren Land","Deciduous Forest","Evergreen Forest","Mixed Forest","Dwarf Scrub","Shrub_Scrub","Grassland_Herbaceous","Sedge_Herbaceous","Lichens","Moss",$
    "Pasture_Hay","Cultivated Crops","Woody Wetlands"," Emergent Herbaceous Wetlands"]

  ;read clipped NLCD data
  infile = "/largedisk_a/tree_canopy/original_data/NLCD_2016_Land_Cover_clip_tcma_tree_canopyr.tif"
  openr, lun, infile, /get_lun
  data_nlcd = bytarr(ns,nl)
  readu, lun, data_nlcd
  free_lun, lun
  array = data_nlcd
  nlcd_classes = array[UNIQ(array, SORT(array))]
  print, nlcd_classes

  result =  fix(data_nlcd)

  for i=0,n_elements(nlcd_classes)-1 do begin
    print, nlcd_classes[i]
    index = where(nlcd_id eq nlcd_classes[i], count)
    ; exclude forest types
    if nlcd_classes[i] ne 41 and nlcd_classes[i] ne 42 and nlcd_classes[i] ne 43 then begin 
      if count eq 1 then begin
        index1 = where(data_tree ne -9999 and data_nlcd eq nlcd_classes[i],count1)
        if count1 gt 100 then begin
          index11 = where(data_tree eq 0 and data_nlcd eq nlcd_classes[i],count11)
          if count11 gt 0 then result[index11] = nlcd_classes[i] *10+1
          index22 = where(data_tree gt 0 and data_tree le 0.33 and data_nlcd eq nlcd_classes[i],count22)
          if count22 gt 0 then result[index22] = nlcd_classes[i] *10+2
          index33 = where(data_tree gt 0.33 and data_tree le 1 and data_nlcd eq nlcd_classes[i],count33)
          if count33 gt 0 then result[index33] = nlcd_classes[i]*10+3
        endif
      endif
    endif
  endfor

  path = "/largedisk_a/tree_canopy/original_data/NLCD_2016_Land_Cover_new_addingtree_Joe.tif"
  WRITE_TIFF,path,result,COMPRESSION=1, GEOTIFF=geotiff_tree,/short

end