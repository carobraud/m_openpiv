#! /bin/bash
# 18/05/2016
# Automatic conversion: NetCDF to Tecplot 
#
dirstat='/media/HDImage/SMARTEOLE/VECTORS/OPENPIV/'

for config in `cat config.txt`
do
    dirin=$dirstat
    file='VECTOR_'$config'_STAT'
    zmm=${file:27:3}
#   recal z
    znew=`echo "-$zmm + 539" | bc`
    znew='z='$znew'mm,'
    flowrate=${file:12:3}
    flowrate=$flowrate'l/min,'
    incidence=${file:20:2}
    incidence=$incidence'degree'

    echo $dirin$file
    echo $znew$flowrate$incidence

    python netcdf2tecplot.py -di $dirin -fi $file'.nc' -fo $file'.dat' -z $znew$flowrate$incidence
    mv $file'.dat' $dirin
done


    


