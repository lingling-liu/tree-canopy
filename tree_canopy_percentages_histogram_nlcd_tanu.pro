pro tree_canopy_percentages_histogram_NLCD_tanu

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
      index1 = where(data_tree ne -9999 and data_nlcd eq nlcd_classes[i],count1)
      if count1 gt 100 then begin
        q++
;        title1 = nlcd_name[index] +"_Tanu"
;        temp1 = data_tree[index1]
;        binsize = 0.1
;        ;binsize = 0.33       
;        pdf1 = HISTOGRAM(temp1, binsize=binsize,LOCATIONS=xbin,max=1,min=0); ge and lt (the last one is equal to 1)
;        
;        ; handle 1 
;        nbar = n_elements(pdf1)
;        pdf2 = pdf1[0:nbar-2]
;        pdf2[nbar-2] = pdf1[nbar-2]+pdf1[nbar-1]
;;        print, pdf1
;;        print, pdf2
;        pdf1 = pdf2
;   
;        ppdf1 = pdf1/(N_ELEMENTS(temp1)-0.0)
;        print,title1
;        print,ppdf1
;
;        p = BARPLOT(ppdf1, NBARS=1,title = title1,$
;          PATTERN_ORIENTATION = 60,PATTERN_SPACING = 3,width=width,FONT_SIZE = 13, $
;          FILL_COLOR=colors[0],YRANGE=[0, 0.8],DIMENSIONS=[400,400])
;          
;        ax = p.axes
;        ax[0].minor = 0
;        ax[0].tickname= [' ','<0.1',' ','0.2-0.3',' ','0.4-0.5',' ','0.6-0.7',' ','0.8-0.9',' ',' ']
;        ax[0].TICKFONT_SIZE =10
;        ; y axis
;        ax[1].minor = 0
;        ax[1].tickinterval= 0.1
;        ;ax[1].title = "Percentage"
;        
;        p.Save,"/largedisk_a/tree_canopy/Fig/histogram_"+title1+'.png',$
;          BORDER=10, RESOLUTION=300, /TRANSPARENT
;        p.close
      endif
    endif
endfor

print,q

  end