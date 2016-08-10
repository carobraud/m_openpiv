#! /bin/bash

dirname=$1
workdir=/home/cbraud/OPEN_PIV/
dirin='/mnt/HDImage/SMARTEOLE/PIV-Nov2015-TIF/'$dirname
#dirin='/home/cbraud/OPEN_PIV/'
dirout='/mnt/HDImage/SMARTEOLE/VECTORS/'
#dirout='/home/cbraud/OPEN_PIV/'
dt=$2
#dt=35 #in microsec
filout='VECTOR'
pattern_a='B00001_0.tif'
pattern_b='B00001_1.tif'
tronc_img=True
display=True

#for dirname in `cat dirname.txt`
#do
cd $dirout
mkdir $dirname
cd $workdir
#dirout=$dirout
dirout=$dirout$dirname

python MultiplePair.py -di=$dirin -do=$dirout -dt=$dt -pa=$pattern_a -pb=$pattern_b -tr=$tronc_img -show=$display




#exit

