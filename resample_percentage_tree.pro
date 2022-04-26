pro resample_percentage_tree

  ; read 2m tree canopy data

  data = READ_TIFF("/largedisk_a/tree_canopy/Tree_canopy_Minneapolis--St-Paul--MN--WI_Tanu.tif",geotiff = geotiff)
  ;print,ESA_data[0,0]

  ns = n_elements(data[*,0])
  nl = n_elements(data[0,*])
  print,ns,nl

  result = fltarr(ns/5,nl/5)-9999

  ;resample 10m
  for i=0,nl/5-1 do begin
    for j=0,ns/5-1 do begin
      ;print,j*5l,(j+1)*5l-1,i*5l,(i+1)*5l-1
      temp = data[j*5l: (j+1)*5l-1,i*5l: (i+1)*5l-1]
      index = where(temp eq 1, count)
      if count ge 0 then begin
        result[j,i] = count/25.0
      endif
    endfor
  endfor

  geotiff.MODELPIXELSCALETAG = [10.0000000000000000, 10.0000000000000000, 0.0000000000000000]
  tiff_file="/largedisk_a/tree_canopy/Tree_canopy_Minneapolis--St-Paul--MN--WI_10m.tif"
  WRITE_TIFF, tiff_file, result, GEOTIFF=geotiff,/float
  
  ;resample 30m
  result = fltarr(ns/15,nl/15)-9999
  
  for i=0,nl/15-1 do begin
    for j=0,ns/15-1 do begin
      ;print,j*5l,(j+1)*5l-1,i*5l,(i+1)*5l-1
      temp = data[j*15l: (j+1)*15l-1,i*15l: (i+1)*15l-1]
      index = where(temp eq 1, count)
      if count ge 0 then begin
        result[j,i] = count/225.0
      endif
    endfor
  endfor

  geotiff.MODELPIXELSCALETAG = [30.0000000000000000, 30.0000000000000000, 0.0000000000000000]
  tiff_file="/largedisk_a/tree_canopy/Tree_canopy_Minneapolis--St-Paul--MN--WI_30m.tif"
  WRITE_TIFF, tiff_file, result, GEOTIFF=geotiff,/float

end


