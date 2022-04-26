pro scatter_plot_anomaly_greenup_onset_temp_lp_3years

  ;1983 greenup onset
  input = "/hunter/data1/liul/PECORA/CONUS/Anomaly/NA_anomaly_CONUS_1983.img"
  ns = 1225
  nl = 650
  data1 = lonarr(ns,nl)
  openr, lun, input, /get_lun
  readu, lun, data1
  free_lun, lun

  ;1983 temp lp
  input = "/hunter/data1/liul/NARR/temp/CONUS/Anomaly/temp_lp_anomaly_CONUS_1983.img"
  ns = 1225
  nl = 650
  data2 = intarr(ns,nl)
  openr, lun, input, /get_lun
  readu, lun, data2
  free_lun, lun

  index = where(data1 ge -30 and data1 le 30 and data2 ge -8000 and data2 le 8000,count)
  temp1 = data1[index]
  temp2 = data2[index]/1000.0 ;temp
  path = '/hunter/data1/liul/PECORA/CONUS/Anomaly/1983_gri_lp.csv'
  write_CSV,path,temp1,temp2

  p = PLOT(temp2,temp1, '.g2', SYM_SIZE = 3.5, FONT_SIZE = 13, _EXTRA = EXTRA_KEYWORDS,xrange=[-9,9],yrange=[-35,35],$
    title = title1, DIMENSIONS=[1200,1000],LAYOUT=[3,0],/CURRENT,MARGIN = [0.25,0.1,0,0.2])
  
  r11 = CORRELATE(temp2,temp1, DOUBLE=KEYWORD_SET(double)) ; Dates
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
  print,'1983',r11,p11
  
  ;1996 greenup onset
  input = "/hunter/data1/liul/PECORA/CONUS/Anomaly/NA_anomaly_CONUS_1996.img"
  ns = 1225
  nl = 650
  data1 = lonarr(ns,nl)
  openr, lun, input, /get_lun
  readu, lun, data1
  free_lun, lun

  ;1996 temp lp
  input = "/hunter/data1/liul/NARR/temp/CONUS/Anomaly/temp_lp_anomaly_CONUS_1996.img"
  ns = 1225
  nl = 650
  data2 = intarr(ns,nl)
  openr, lun, input, /get_lun
  readu, lun, data2
  free_lun, lun

  index = where(data1 ge -30 and data1 le 30 and data2 ge -8000 and data2 le 8000,count)
  temp1 = data1[index]
  temp2 = data2[index]/1000.0 ;temp
  path = '/hunter/data1/liul/PECORA/CONUS/Anomaly/1996_gri_lp.csv'
  write_CSV,path,temp1,temp2

  p = PLOT(temp2,temp1, '.g2', SYM_SIZE = 3.5, FONT_SIZE = 13, _EXTRA = EXTRA_KEYWORDS,xrange=[-9,9],yrange=[-35,35],$
    title = title1, DIMENSIONS=[1200,1000],LAYOUT=[3,0],/CURRENT,MARGIN = [0.25,0.1,0,0.2])

  r11 = CORRELATE(temp2,temp1, DOUBLE=KEYWORD_SET(double)) ; Dates
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
  print,'1996',r11,p11


  ;2012 greenup onset
  input = "/hunter/data1/liul/PECORA/CONUS/Anomaly/NA_anomaly_CONUS_2012.img"
  ns = 1225
  nl = 650
  data1 = lonarr(ns,nl)
  openr, lun, input, /get_lun
  readu, lun, data1
  free_lun, lun

  ;2012 temp lp
  input = "/hunter/data1/liul/NARR/temp/CONUS/Anomaly/temp_lp_anomaly_CONUS_2012.img"
  ns = 1225
  nl = 650
  data2 = intarr(ns,nl)
  openr, lun, input, /get_lun
  readu, lun, data2
  free_lun, lun

  index = where(data1 ge -30 and data1 le 30 and data2 ge -8000 and data2 le 8000,count)
  temp1 = data1[index]
  temp2 = data2[index]/1000.0 ;temp
  path = '/hunter/data1/liul/PECORA/CONUS/Anomaly/2012_gri_lp.csv'
  write_CSV,path,temp1,temp2
  
  p = PLOT(temp2,temp1, '.g2', SYM_SIZE = 3.5, FONT_SIZE = 13, _EXTRA = EXTRA_KEYWORDS,xrange=[-9,9],yrange=[-35,35],$
    title = title1, DIMENSIONS=[1200,1000],LAYOUT=[3,0],/CURRENT,MARGIN = [0.25,0.1,0,0.2])

  r11 = CORRELATE(temp2,temp1, DOUBLE=KEYWORD_SET(double)) ; Dates
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
  print,'2012',r11,p11
  
  
end