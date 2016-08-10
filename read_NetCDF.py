from Scientific.IO.NetCDF import NetCDFFile 
#from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

class read_netcdf:
    """Read parameters class, reads parameters used in openpiv software"""
    def __init__(self,filename):
#        self.fp=filename
        self.ncfile = NetCDFFile(filename,'r') 
        
    def piv_process(self):
        piv = self.ncfile.variables['piv_process']
        #    print("dt=",piv.dt)
        #    print("Window size =",piv.windowsize)
        return piv

    def image(self):
        image=self.ncfile.variables['image']
        return image

    def filters(self):
        filters=self.ncfile.variables['filters']
        return filters

    def save(self):
        save=self.ncfile.variables['save']
        return save

    def readpiv(self):
        ux=self.ncfile.variables['ux'][:]
        uy=self.ncfile.variables['uy'][:]
        flag=self.ncfile.variables['flag'][:]
        xvar=self.ncfile.variables['xvar'][:]
        yvar=self.ncfile.variables['yvar'][:]        
        return xvar,yvar,ux,uy,flag


if __name__ == '__main__':
    
    readparameterfile=0
    readpivdata=1
    translateaxis=1

    if (readpivdata == 1):
    #define name of the file
        filename='VECTOR_10ms_260lmin_05deg_z536mm_dt35us.nc'
    #create object
        read_param=read_netcdf(filename)
        # Read piv data type:
        xvar,yvar,ux,uy,flag=read_param.readpiv()
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
