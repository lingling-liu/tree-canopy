pro tree_canopy_reclassify_tanu

  ; read tree canopy percentages
  
  ns = 2790
  nl = 2899
  
  infile = "/largedisk_a/tree_canopy/original_data/Tree_canopy_Minneapolis--St-Paul--MN--WI_Tanu_UTM.tif"
  openr, lun, infile, /get_lun
  data_tree = fltarr(ns,nl)
  readu, lun, data_tree
  free_lun, lun
  index_none =  where(data_tree eq -9999)
 
  
  

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
  
  ;get map_info
  envi_open_file,infile,r_fid=fid1
  IF (fid1 EQ -1) THEN BEGIN
    ENVI_BATCH_EXIT
    RETURN
  ENDIF

  ENVI_FILE_QUERY,fid1, dims=dims1, nb=nb1,ns=ns1,nl=nl1,bnames=bnames1
  map_info =  envi_get_map_info(fid=fid1)
  envi_file_mng,id=fid1,/remove
  
  
  result =  fix(data_nlcd)
  result[index_none] = -9999; no reclassification without tree canopy data

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
  
  path = "/largedisk_a/tree_canopy/original_data/NLCD_2016_Land_Cover_new_addingtree_Tanu.img"
  if (path eq '') then return
  OpenW, unit, path, /Get_LUN
  
  writeu,unit,result
  free_lun,unit
  ENVI_SETUP_HEAD, fname=strmid(path,0,strlen(path)-4), $
    ns=ns, nl=nl, nb=1,$
    data_type=2,INTERLEAVE =2, $
    offset=0,map_info=map_info,/write

  end