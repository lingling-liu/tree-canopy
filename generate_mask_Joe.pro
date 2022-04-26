pro generate_mask_Joe

  ; read 2m tree canopy data

  ;data = READ_TIFF("/largedisk_a/tree_canopy/tcma_lc_finalv1_2015.tif",geotiff = geotiff)
  data = READ_TIFF("/largedisk_a/tree_canopy/original_data/tcma_lc_treecanopy_v1.tif",geotiff = geotiff)
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
      if count ge 0 then begin
        result[j,i] = count/100.0
      endif
    endfor
  endfor

  ;  geotiff.MODELPIXELSCALETAG = [10.0000000000000000, 10.0000000000000000, 0.0000000000000000]
  ;  tiff_file="/largedisk_a/tree_canopy/tcma_lc_treecanopy_10m.tif"
  ;  WRITE_TIFF, tiff_file, result, GEOTIFF=geotiff,/float

  ;resample 30m
  result = fltarr(ns/30,nl/30)

  for i=0,nl/30-1 do begin
    for j=0,ns/30-1 do begin
      ;print,j*5l,(j+1)*5l-1,i*5l,(i+1)*5l-1
      temp = data[j*30l: (j+1)*30l-1,i*30l: (i+1)*30l-1]
      index_0 = where(temp eq 0, count_0) ; boudary for valid data
      if count_0 lt 200 then begin
        result[j,i] = 1
;        index = where(temp eq 6 or temp eq 7, count)
;        if count ge 0 then begin
;          result[j,i] = count/900.0
;        endif
      endif
    endfor
  endfor

  geotiff.MODELPIXELSCALETAG = [30.0000000000000000, 30.0000000000000000, 0.0000000000000000]
  tiff_file="/largedisk_a/tree_canopy/tcma_lc_treecanopy_30m_mask.tif"
  WRITE_TIFF, tiff_file, result, GEOTIFF=geotiff,/float

end


