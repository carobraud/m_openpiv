#! /bin/bash
# 26/05/2016
# tecplot to png images using a given layout
#


for config in `cat config.txt`
do
    cp macro_template.mcr macro.mcr
    dirin="/media/HDImage/SMARTEOLE/VECTORS/OPENPIV"
    filin="VECTOR_"$config"_STAT.dat"
    echo 'FILIN='$filin
    layout="test_layout_tecplot.lay"
    filout="PLOT_"$config".png"
    sed -e "s%DIRIN%$dirin%g" macro.mcr > temp1.mcr
    sed -e "s%FILIN%$filin%g" temp1.mcr > temp2.mcr
    sed -e "s%LAYOUTFILE%$layout%g" temp2.mcr > temp3.mcr
    sed -e "s%FILOUT%$filout%g" temp3.mcr > macro.mcr
    tecplot -b -p macro.mcr
done
#while read line
#do
#    eval echo "$line"
#done < "macro.mcr"




