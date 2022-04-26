pro scatter_plot_Joe_NASA_tree_canopy_data

; Read Joe's data
tiff_file="/largedisk_a/tree_canopy/original_data/30m/tcma_lc_treecanopy_30m.tif"
Joe_data = READ_TIFF(tiff_file,geotiff = geotiff)
ns = n_elements(Joe_data[*,0])
nl = n_elements(Joe_data[0,*])



; Read NASA 30 m data
infile = "/largedisk_a/tree_canopy/original_data/30m/Tree_canopy_NASA_30m_MN_UTM_re.tif"
openr, lun, infile, /get_lun
NASA_data =  bytarr(ns,nl)
readu, lun,NASA_data 
free_lun, lun


; read mask data
tiff_file="/largedisk_a/tree_canopy/tcma_lc_treecanopy_30m_mask.tif"
mask_data = READ_TIFF(tiff_file,geotiff = geotiff)

index = where(mask_data eq 1, count)

X = Joe_data[index]*100
Y = NASA_data[index]



p = PLOT(X,Y, '.g2', SYM_SIZE = 3.5, FONT_SIZE = 13, _EXTRA = EXTRA_KEYWORDS,xrange=[0,100],yrange=[0,100],$
  title = "Joe vs NASA", DIMENSIONS=[600,600])
 

r11 = CORRELATE(X,Y, DOUBLE=KEYWORD_SET(double)) ; Dates
; compute the degrees of freedom
df = count - 2
if (1.0 - r11 le 1.0E-7) then begin
  p11 = 0.0
endif else begin
  ; compute the t statistic
  t = r11/sqrt((1.0-r11*r11)/FLOAT(df))
  ; calculate the two-side 'tail area' probability
  p11 = 2.0 * (1.0 - T_PDF(ABS(t), df))
endelse
print,r11*r11,p11








end