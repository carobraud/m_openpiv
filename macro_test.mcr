#!MC 1410
$!VarSet |MFBD| = '/home/braud/data/Eolien/SMARTEOLE/TESTS-@PRISME/PIV/OPEN_PIV'
$!READDATASET  '"/media/HDImage/SMARTEOLE/VECTORS/OPENPIV/VECTOR_10ms_220lmin_05deg_z532mm_dt35us_STAT.dat" '
  READDATAOPTION = NEW
  RESETSTYLE = YES
  VARLOADMODE = BYNAME
  ASSIGNSTRANDIDS = YES
  VARNAMELIST = '"\'xvar\'" "\'yvar\'" "\'uavg\'" "\'vavg\'" "\'u2avg\'" "\'v2avg\'" "\'u3avg\'" "\'v3avg\'" "\'u4avg\'" "\'v4avg\'" "\'u2nrm\'" "\'v2nrm\'" "\'u3nrm\'" "\'v3nrm\'" "\'u4nrm\'" "\'v4nrm\'"'
$!PICK SETMOUSEMODE
  MOUSEMODE = SELECT
$!PAGE NAME = 'Untitled'
$!PAGECONTROL CREATE
$!PICK SETMOUSEMODE
  MOUSEMODE = SELECT
$!OPENLAYOUT  "/media/HDImage/SMARTEOLE/VECTORS/OPENPIV/test_layout_tecplot.lay"
$!PRINTSETUP PALETTE = COLOR
$!EXPORTSETUP IMAGEWIDTH = 686
$!EXPORTSETUP EXPORTFNAME = '/home/braud/data/Eolien/SMARTEOLE/TESTS-@PRISME/PIV/OPEN_PIV/VECTOR_10ms_220lmin_05deg_z532mm.png'
$!EXPORT 
  EXPORTREGION = CURRENTFRAME
$!RemoveVar |MFBD|
