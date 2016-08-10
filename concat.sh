#!/bin/bash

# 18/02/2016
# Concat NetCDF files + do basic STATISTICS
# (see /home/braud/code/code.nco/stat3Cnc.SbyS.sh)

u=ux
v=uy
grids='xvar,yvar'


#list=
#for((slice=0,imin=0,imax=sizeSlice-1;slice<nbSlice;slice++,imin+=sizeSlice,imax+=sizeSlice))
#do
#bin=/home/braud/bin/
#config='10ms_000lmin_00deg_z539mm_dt35us'

#config=$1
dirbase='/media/HDImage/SMARTEOLE/VECTORS/OPENPIV/'
for config in `cat config.txt`
do
    dir=$dirbase'PIV_'$config'_1000im/'

##prepare variable file
    /bin/echo -n -e '\r preparing file \n'
    base='VECTOR_ALL.nc'
    tmp='VECTOR_TEMP.nc'
    out='VECTOR_STAT.nc'
    ncecat -O $dir'VECTOR_0001.nc' $dir$base # create an unlimited dimension
    ncecat -A $dir'VECTOR_'[0-2]???'.nc' $dir$base # concatenate samples 
#    ncecat -A $dir'VECTOR_000'[0-1]'.nc' $dir$base # concatenate samples 
    ncrename -O -v $u,u -v $v,v $dir$base # Rename variables
  ## mean m1' (1rst central moment m1=0)
    /bin/echo -n -e '\rcomputing mean \n'
    ncwa -O -a record $dir$base $dir$tmp # Compute record mean of u,v
    ncrename -O -v u,uavg -v v,vavg $dir$tmp # Rename to avoid conflict
    cp $dir$base $dir$out # copy original base with u,v variable name
    ncks -A -v uavg,vavg $dir$tmp $dir$out # Append means with original base
  ## 2nd central moment m2=S(v^2-m^2)=m2'-m1'^2 (variance) 
  ## -->Demo: u'=(u-umean)²=u²+umean²-2(uumean) -->uvar=mean(u'^2)=mean(u^2)+umean^2-2*umean*umean=mean(u^2)-umean²
    /bin/echo -n -e '\rcomputing variance \n'  
    ncap -O -s "uvar=u^2-uavg^2" -s "vvar=v^2-vavg^2" $dir$out $dir$tmp # Variance
    ncwa -O -a record -v uvar,vvar $dir$tmp $dir$tmp # record-mean variance
    ncrename -O -v uvar,u2avg -v vvar,v2avg $dir$tmp # Rename to avoid conflict
    ncks -A -v u2avg,v2avg $dir$tmp $dir$out # Append mean variance with original base
  ##covariance
    /bin/echo -n -e '\rcomputing covariance \n'
    ncap -O -s "uprmvprm=u*v-uavg*vavg" $dir$out $dir$tmp # Covariance
    ncwa -O -a record -v uprmvprm $dir$tmp $dir$tmp # Time-mean covariance
    ncrename -O -v uprmvprm,uvavg $dir$tmp # Rename to avoid conflict
    ncks -A -v uvavg $dir$tmp $dir$out # Place time-mean covariance with originals (append)
  ##3rd central moment m3=S(v^3-m^3)=m3'-3*m1'*m2'+2*m1'^3 (Skewness)
    /bin/echo -n -e '\rcomputing skewness \n'
    ncap -O -s "uvar=(u-uavg)^3" -s "vvar=(v-vavg)^3" $dir$out $dir$tmp # Variance
    ncwa -O -a record -v uvar,vvar $dir$tmp $dir$tmp # Time-mean variance
    ncrename -O -v uvar,u3avg -v vvar,v3avg $dir$tmp # Rename to avoid conflict
    ncks -A -v u3avg,v3avg $dir$tmp $dir$out # Place time-mean variance with originals (append)
  ##4rd central moment m4=S(v^4-m^4)= (Kurtosis)
    /bin/echo -n -e '\rcomputing kurtosis \n'
    ncap -O -s "uvar=(u-uavg)^4" -s "vvar=(v-vavg)^4" $dir$out $dir$tmp # Variance
    ncwa -O -a record -v uvar,vvar $dir$tmp $dir$tmp # Time-mean variance
    ncrename -O -v uvar,u4avg -v vvar,v4avg $dir$tmp # Rename to avoid conflict
    ncks -A -v u4avg,v4avg $dir$tmp $dir$out # Place time-mean variance with originals (append)
  ##remove variables
    ncks -O -h -v $grids $dir$base $dir$tmp
    ncks -A -h -a -v uavg,vavg,u2avg,v2avg,uvavg,u3avg,v3avg,u4avg,v4avg $dir$out $dir$tmp
    mv $dir$tmp $dir$out
  ##print variables
    ncdump -h $dir$out | head -n 18


#make UNLIMITED
#$bin/ncmulr.sh $f $f $dim

#normalise
    ncap -O \
	-s "u2nrm=sqrt(u2avg)"     -s "v2nrm=sqrt(v2avg)"      \
	-s "u3nrm=u3avg/u2avg^1.5" -s "v3nrm=v3avg/v2avg^1.5"  \
	-s "u4nrm=u4avg/u2avg^2"   -s "v4nrm=v4avg/v2avg^2"    \
	$dir$out $dir$out

#show result information
#ncdump -h $dir$out | head -n 14

#reverse around x axis 
    ncpdq -O -a -x $dir$base $dir$base 
    ncpdq -O -a -x $dir$out $dir$out
# rename x and y dimensions
    ncrename -O -d x,xtemp $dir$out $dir$out 
    ncrename -O -d y,ytemp $dir$out $dir$out 
    ncrename -O -d xtemp,y $dir$out $dir$out 
    ncrename -O -d ytemp,x $dir$out $dir$out 
    ncrename -O -d x,xtemp $dir$base $dir$base 
    ncrename -O -d y,ytemp $dir$base $dir$base 
    ncrename -O -d xtemp,y $dir$base $dir$base 
    ncrename -O -d ytemp,x $dir$base $dir$base 
# erase history attribute

# Put attributes to instanteous field data
    ncatted -O -a long_name,u,o,c,instantaneous_streamwise_velocity $dir$base
    ncatted -O -a units,u,o,c,m/s $dir$base
    ncatted -O -a long_name,v,o,c,instantaneous_spanwise_velocity $dir$base
    ncatted -O -a units,v,o,c,m/s $dir$base
    ncatted -O -a long_name,flag,o,c,flag_number $dir$base
#ncatted -O -a quanta,flag,o,s,"0,1,2,16" VECTOR_ALL.nc out.nc

# Put attributes to statistical field 
    ncatted -O -a long_name,u2nrm,o,c,normalized_variance_streamwise_velocity $dir$out
    ncatted -O -a units,u2nrm,o,c,norm_by_rms-u $dir$out
    ncatted -O -a long_name,v2nrm,o,c,normalized_variance_spanwise_velocity $dir$out
    ncatted -O -a units,v2nrm,o,c,norm_by_rms-v $dir$out
    ncatted -O -a long_name,u3nrm,o,c,normalized_skewness_streamwise_velocity $dir$out
    ncatted -O -a units,u3nrm,o,c,norm_by_var-u-1-5 $dir$out
    ncatted -O -a long_name,v3nrm,o,c,normalized__skewness_spanwise_velocity $dir$out
    ncatted -O -a units,v3nrm,o,c,norm_by_var-v-1-5 $dir$out
    ncatted -O -a long_name,u4nrm,o,c,normalized_kurtosis_streamwise_velocity $dir$out
    ncatted -O -a units,u4nrm,o,c,norm_by_var-u-2 $dir$out
    ncatted -O -a long_name,v4nrm,o,c,normalized_kurtosis_spanwise_velocity $dir$out
    ncatted -O -a units,v4nrm,o,c,norm_by_var-v-2 $dir$out
    ncatted -O -a long_name,uavg,o,c,mean_streamwise_velocity $dir$out
    ncatted -O -a units,uavg,o,c,m/s $dir$out
    ncatted -O -a long_name,vavg,o,c,mean_spanwise_velocity $dir$out
    ncatted -O -a units,vavg,o,c,m/s $dir$out
    ncatted -O -a long_name,u2avg,o,c,variance_streamwise_velocity $dir$out
    ncatted -O -a units,u2avg,o,c,m²/s² $dir$out
    ncatted -O -a long_name,v2avg,o,c,variance_spanwise_velocity $dir$out
    ncatted -O -a units,v2avg,o,c,m²/s² $dir$out
    ncatted -O -a long_name,u3avg,o,c,skewness_streamwise_velocity $dir$out
    ncatted -O -a units,u3avg,o,c,m³/s³ $dir$out
    ncatted -O -a long_name,v3avg,o,c,skewness_spanwise_velocity $dir$out
    ncatted -O -a units,v3avg,o,c,m³/s³ $dir$out
    ncatted -O -a long_name,u4avg,o,c,kurtosis_streamwise_velocity $dir$out
    ncatted -O -a units,u4avg,o,c,m⁴/s⁴ $dir$out
    ncatted -O -a long_name,v4avg,o,c,kurtosis_spanwise_velocity $dir$out
    ncatted -O -a units,v4avg,o,c,m⁴/s⁴ $dir$out


#delete history in the global attribute
    ncatted -O -a history,global,d,,''  $dir$base
    ncatted -O -a history,global,d,,''  $dir$out

## modify coordinates
    /bin/echo -n -e '\rcoordinates \n'
    ncap -O -s "xvar=xvar/0.3+0.860" -s  "yvar=yvar/0.3-0.2255" $dir$base $dir$base
#    ncap -O -s "xvar=xvar/0.3+0.975" -s  "yvar=yvar/0.3-0.2255" $dir$base $dir$base
    ncwa -O -a record $dir$out $dir$out # Time-mean
    ncap -O -s "xvar=xvar/0.3+0.860" -s  "yvar=yvar/0.3-0.2255" $dir$out $dir$out
#    ncap -O -s "xvar=xvar/0.3+0.975" -s  "yvar=yvar/0.3-0.2255" $dir$out $dir$out

# attributes for x and y variables
    /bin/echo -n -e '\rattributes for x and y variables \n'
    ncatted -O -a long_name,xvar,o,c,streamwise_direction $dir$base
    ncatted -O -a units,xvar,o,c,x/c_0_at_LE $dir$base
    ncatted -O -a long_name,yvar,o,c,spanwise_direction $dir$base
    ncatted -O -a units,yvar,o,c,y/c_0_at_LE $dir$base
    ncatted -O -a long_name,xvar,o,c,streamwise_direction $dir$out
    ncatted -O -a units,xvar,o,c,x/c_0_at_LE $dir$out
    ncatted -O -a long_name,yvar,o,c,spanwise_direction $dir$out
    ncatted -O -a units,yvar,o,c,y/c_0_at_LE $dir$out
# Zip instantenous file
    zip 'VECTOR_'$config'_ALL.zip' $dir$base
    mv 'VECTOR_'$config'_ALL.zip' $dirbase
    mv $dir$out $dirbase'VECTOR_'$config'_STAT.nc'
    rm $dir$base	
done

