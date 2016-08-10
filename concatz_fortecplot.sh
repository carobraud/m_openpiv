#! /bin/bash
# 18/05/2016
# concat zones of tecplot files
# 

#TODO
#flowrate=260
#flowrate=$1


dirin=/media/HDImage/SMARTEOLE/VECTORS/OPENPIV/
file0=$dirin'VECTOR_10ms_260lmin_05deg_z530mm_dt35us_STAT.dat'
rm temp.dat
temp=temp.dat
cp $file0 $temp
mv $temp $dirin


for file in `cat config.txt` 
do 
echo $file'.dat'

tail -n +3 $dirin'VECTOR_'$file'_STAT.dat' >> $dirin$temp 
done

mv $dirin$temp $dirin'VECTOR_10ms_260lmin_05deg_STAT.dat'
