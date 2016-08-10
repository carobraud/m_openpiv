#!/usr/bin/python
# -*- coding: utf-8 -*-

from Scientific.IO.NetCDF import NetCDFFile 
#from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os.path


class read_object:
    """Read parameters class, reads parameters used in openpiv software"""
    def __init__(self,filename):
#        self.fp=filename
        self.ncfile = NetCDFFile(filename,'r') 
        #todo: ADD data and data_name

### TODO: automatic read of attributes --> to test 
#    def read_param(self,param_name)
#    # extract number of parameter to read
#        tmp=np.array(param_name).shape           
#        npar=tmp[0]
#        param=[]
#        for k in range(0,npar):
#            param.append(self.ncfile.variables[param_name[k]][:])
#        return param

    def piv_process(self):
        """Read parameters used for PIV processing"""
        piv = self.ncfile.variables['piv_process']
        #    print("dt=",piv.dt)
        #    print("Window size =",piv.windowsize)
        return piv

    def image(self):
        """Read parameters for image treatment"""
        image=self.ncfile.variables['image']
        return image

    def filters(self):
        """Read parameters for filters"""
        filters=self.ncfile.variables['filters']
        return filters

    def save(self):
        """Read parameters to save results"""
        save=self.ncfile.variables['save']
        return save

#TODO: put data and data_name in global variables of the class 
    def read_data(self,data_name):
        """Read a netcdf file with variable number and size of data that are named data name"""
        # extract dim of variables
        tmp=np.array(data_name).shape           
        nvar=tmp[0]
        print 'number of variables:',nvar
        data=[]
        for k in range(0,nvar):
            data.append(self.ncfile.variables[data_name[k]][:])
            
        return data

#TODO: add read_data function --> and define a new function netcdf2tecplot 
    def tecplot(self,data,data_name,filout,zone_name):
        """Write nvar variable in tecplot format"""

        # extract dim of data set
        nvar,nx,ny=np.array(data).shape           
        # open new file
        thefile=open(filout,"w")
        ######## write tecplot header

        ## write title
        thefile.write('TITLE = "{0}"\n'.format(zone_name))

        ## concatenate name of variables
        name_temp=''
        for k in range(0,nvar-1):
            name_temp=name_temp+"'"+str(data_name[k])+"',"

        name_temp=name_temp+"'"+str(data_name[nvar-1])+"'"

        ## write name of variables 
        theformat="VARIABLES ={0}\n"                
        thefile.write(theformat.format(name_temp))

        ## write zone
        thefile.write('ZONE T="{0}", I={1}, J={2}, F=POINT\n'.format(zone_name,ny,nx))
                
        ######### write data 
        theformat="{0}"                
        for i in range(0,nx):
            for j in range(0,ny):
                for k in range(0,nvar):
#                    print np.array(variables[k][i,j])
                    thefile.write(theformat.format(np.array(data[k][i,j])))                   
                    thefile.write("\t")
                                  
                thefile.write("\n")
                
        thefile.close()    
                            
# NOTTODO: TODO IN BASH INSTEAD
#    def tecplot3D2C(self,piv3D2C,filout,zvalue):
#        """Write a typical piv data set 3D2C for tecplot"""

if __name__ == '__main__':

 
    readparameterfile=0
    readpivdata=0
    translateaxis=0
    tecplotPIV2D2C=0
    tecplot=1
    inst=0
    mean=1
    if (tecplot == 1):
        if (inst == 1):
            # Location of instaneous data
            dirin='/home/braud/data/Eolien/SMARTEOLE/TESTS-@PRISME/PIV-DATA/VECTORS/OPENPIV/PIV_10ms_000lmin_05deg_z539mm_dt35us_1000im/'
            filin='VECTOR_0495.nc'        
            filename=os.path.join(dirin,filin)
            #create object
            read=read_object(filename)
            # Define variable to read:        
            var_name=np.array(['xvar','yvar','ux','uy','flag']) 
            # read variables
            var=read.read_data(var_name)
            #convert to tecplot
            read.tecplot(var,var_name,'fileout.dat','z536mm')
        if (mean == 1):
            # Location of mean data
            dirin='/home/braud/data/Eolien/SMARTEOLE/TESTS-@PRISME/PIV-DATA/VECTORS/OPENPIV'
            filin='VECTOR_10ms_260lmin_05deg_z536mm_dt35us_STAT.nc'        
            filename=os.path.join(dirin,filin)
            #create object
            read=read_object(filename)
            # Define variable to read:        
            var_name=np.array(['xvar','yvar','uavg','vavg','u2avg','v2avg','u3avg','v3avg','u4avg','v4avg','u2nrm','v2nrm','u3nrm','v3nrm','u4nrm','v4nrm']) 
            # read variables
            var=read.read_data(var_name)
            # replace nan numbers by 0 (done only for normilized variables of third order)
            var=np.nan_to_num(var)
            #convert to tecplot
            read.tecplot(var,var_name,'fileout.dat','z536mm')

    if (tecplotPIV2D2C == 1):
    #define name of the file
        dirin='/home/braud/data/Eolien/SMARTEOLE/TESTS-@PRISME/PIV-DATA/VECTORS/OPENPIV'
        filin='VECTOR_10ms_260lmin_05deg_z536mm_dt35us_STAT.nc'
        filename=os.path.join(dirin,filin)
#        print filename
        #create object
        read=read_object(filename)
        # Read piv data type:        
        piv2D2C=['xvar','yvar','uavg','vavg','xvar'] #!! no flag in STAT file: replace by xvar for instance
        xtemp,ytemp,ux,uy,flag=read.piv_data(piv2D2C)
        # set x=0 at the trailing edge
        chord=0.3
        decalx=-0.860
        decaly=0.2255
        X=xtemp/chord-decalx
        Y=ytemp/chord-decaly
        # prepare to convert to tecplot
        nx,ny=ux.shape
        flag=np.zeros(ux.shape) # no flag in STAT
        
        piv2D2C_data=X,Y,ux,uy,flag
#       for i in range(0,nvar):
#           x,y,ux,uy,flag.append(piv2D2C[i])

        #convert to tecplot
        read.tecplot2D2C(piv2D2C_data,'fileout.dat','z536mm')

    if (readpivdata == 1):
    #define name of the file
        filename='VECTOR_10ms_260lmin_05deg_z536mm_dt35us.nc'
    #create object
        read=read_object(filename)
        # Read piv data type:
        xvar,yvar,ux,uy,flag=read.piv_data()
        Q=plt.quiver(xvar,yvar,ux-10.,uy, angles='xy', scale=300,headwidth=2, headlength=2)
        plt.imshow(ux-10.,interpolation='bicubic',vmin=-12.,vmax=8.,extent=[xvar.min(),xvar.max(),yvar.min(),yvar.max()])
        plt.show()
        if (translateaxis == 1):
            filin='/home/braud/doc/VALORISATION/congres/TORQUE/TORQUE_2016/fig/profilNACA65-4-421CC.dat'
            open(filin, "r")
            xcc,ycc=np.loadtxt(filin, skiprows=1,unpack=True)
            chord=0.3
            decalx=-0.860
            decaly=0.2255
            X=xvar/chord-decalx
            Y=yvar/chord-decaly
            Q=plt.quiver(X,Y,ux,uy, angles='xy', scale=300,headwidth=2, headlength=2)
            plt.imshow(ux,interpolation='bicubic',vmin=-2.,vmax=18.,extent=[X.min(),X.max(),Y.min(),Y.max()])
            plt.plot(xcc,ycc)
            plt.show()

    if (readparameterfile == 1):
    #define name of the file
        filename='parameters.nc'
    #create object
        read_param=read_parameters(filename)
        # Read all parameters
        piv_param=read_param.piv_process()
        print("piv parameters",piv_param)
        image_param=read_param.image()
        print ("image parameters",image_param)
        filters_param=read_param.filters()
        print ("filter parameters",filters_param)
        save_param=read_param.save()
        print ("save parameters",save_param)

        print ("read attribute example",filters_param.threshold_flagnum)
        print ("read attribute example",filters_param.threshold_flagnum[0])
        print ("read attribute example",filters_param.show_histogram[0])
        print ("read char attribute",image_param.mask_dirname)
        print ("read char attribute",image_param.mask_filename)
