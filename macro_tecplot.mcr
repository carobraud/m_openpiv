#!MC 1410
$!VarSet |MFBD| = '/media/HDImage/SMARTEOLE/VECTORS/OPENPIV'
$!READDATASET  '"|MFBD|/VECTOR_10ms_000lmin_05deg_z532mm_dt35us_STAT.dat" '
$!OPENLAYOUT  "|MFBD|/test_layout_tecplot.lay"
$!EXPORTSETUP EXPORTFNAME = 'tiiii.png'
$!EXPORT 
  EXPORTREGION = CURRENTFRAME
$!RemoveVar |MFBD|