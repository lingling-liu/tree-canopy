pro tree_canopy_check_none_tanu

  ; read tree canopy percentages
  
  ns = 2790
  nl = 2899
  
  infile = "/largedisk_a/tree_canopy/original_data/Tree_canopy_Minneapolis--St-Paul--MN--WI_Tanu_UTM.tif"
  openr, lun, infile, /get_lun
  data_tree = fltarr(ns,nl)
  readu, lun, data_tree
  free_lun, lun
 

  nlcd_id = [12,21,22,23,24,31,41,42,43,51,52,71,72,73,74,81,82,90,95]
  print,n_elements(nlcd_id)
  nlcd_name = ["Perennial Ice/Snow","Developed, Open Space","Developed, Low Intensity","  Developed, Medium Intensity","Developed High Intensity",$
    " Barren Land","Deciduous Forest","Evergreen Forest","Mixed Forest","Dwarf Scrub","Shrub_Scrub","Grassland_Herbaceous","Sedge_Herbaceous","Lichens","Moss",$
    "Pasture_Hay","Cultivated Crops","Woody Wetlands"," Emergent Herbaceous Wetlands"]

  ;read clipped NLCD data
  infile = "/largedisk_a/tree_canopy/original_data/NLCD_2016_Land_Cover_clip_Tanu.tif"
  openr, lun, infile, /get_lun
  data_nlcd = bytarr(ns,nl)
  readu, lun, data_nlcd
  free_lun, lun
  array = data_nlcd
  nlcd_classes = array[UNIQ(array, SORT(array))]
  print, nlcd_classes


  colors = ['Red']
  q=0
  for i=0,n_elements(nlcd_classes)-1 do begin
    index = where(nlcd_id eq nlcd_classes[i], count)
    if count eq 1 then begin     
      index1 = where(data_tree eq 0 and data_nlcd eq nlcd_classes[i],count1)
      title1 = nlcd_name[index] +"_Tanu"
      print,title1,count1
    endif
endfor

print,q

  end