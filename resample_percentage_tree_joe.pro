pro resample_percentage_tree_joe

  ; read 2m tree canopy data

  data = READ_TIFF("/largedisk_a/tree_canopy/tcma_lc_finalv1_2015.tif",geotiff = geotiff)
  ;print,ESA_data[0,0]

  ns = n_elements(data[*,0])
  nl = n_elements(data[0,*])
  print,ns,nl

  result = fltarr(ns/10,nl/10)-9999

  ;resample 10m
  for i=0,nl/10-1 do begin
    for j=0,ns/10-1 do begin
      ;print,j*5l,(j+1)*5l-1,i*5l,(i+1)*5l-1
      temp = data[j*10l: (j+1)*10l-1,i*10l: (i+1)*10l-1]
      index = where(temp eq 6 or temp eq 7, count)
      if count gt 0 then begin
        result[j,i] = count/100.0
      endif
    endfor
  endfor

  geotiff.MODELPIXELSCALETAG = [10.0000000000000000, 10.0000000000000000, 0.0000000000000000]
  tiff_file="/largedisk_a/tree_canopy/tcma_lc_finalv1_2015_10m.tif"
  WRITE_TIFF, tiff_file, result, GEOTIFF=geotiff,/float
  
  ;resample 30m
  result = fltarr(ns/30,nl/30)-9999
  
  for i=0,nl/30-1 do begin
    for j=0,ns/30-1 do begin
      ;print,j*5l,(j+1)*5l-1,i*5l,(i+1)*5l-1
      temp = data[j*30l: (j+1)*30l-1,i*30l: (i+1)*30l-1]
      index = where(temp eq 6 or temp eq 7, count)
      if count gt 0 then begin
        result[j,i] = count/900.0
      endif
    endfor
  endfor

  geotiff.MODELPIXELSCALETAG = [30.0000000000000000, 30.0000000000000000, 0.0000000000000000]
  tiff_file="/largedisk_a/tree_canopy/tcma_lc_finalv1_2015_30m.tif"
  WRITE_TIFF, tiff_file, result, GEOTIFF=geotiff,/float

end


