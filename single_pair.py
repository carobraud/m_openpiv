#!/usr/bin/python
# PIV processing for a single pair
# todo: 
# 1/ $ncgen -o parameters.nc parameters.cdl
# 2/ $python single_pair.py 
# or $ncgen -o parameters.nc parameters.cdl; python single_pair.py 


import openpiv.tools
import openpiv.scaling
import openpiv.process
import numpy as np
#from math import exp,expm1
#import pylab as plt
import matplotlib.pyplot as plt
#import matplotlib as plt
#from matplotlib import cm 
import pandas as pd
import os.path 
#from numpy import asarray as ar 
import sys
import scipy
from skimage import filters, io
from matplotlib import cm

# Function to read mask (from dantec software)
#import read_mask --> now in filters.py file
# Function to filter signals
import filters
# Function to read parameters from .cdl file
import netcdf_tools 
# Function to write in NetCDF
import write_NetCDF

def SinglePair(args, dirin=".",dirout=".",filout="test",fp="parameters.nc",pattern_a="B0????_0.tif",pattern_b="B0????_1.tif"):
    """A function to do a PIV treatment for a single image Pair  
  
        Parameters
        ----------
        args : tuple
	dirout: str
	        Output directory
	filout: str
	        Output file
        fp: str
	        Input parameter file
    """

    file_a, file_b, counter = args

# Print informations
    print "Name Image, first exposition  : ",file_a
    print "Name Image, second exposition  : ",file_b
    print "Output File's name  : ",filout
    print "Output File's directory : ",dirout


#read parameters from a NetCD file:
# !!! NOT OPTIMUM BECAUSE FILE IS READ EVERY IMAGE PAIR ... TODO: class in Multiple.py ? !!!
    #read object
    read_param=netcdf_tools.read_object(fp)
    
    #LOAD AND PRINT PARAMETERS:
    #PIV
    piv_param=read_param.piv_process()
    print("piv parameters",piv_param)
    #IMAGE
    image_param=read_param.image()
    print ("image parameters",image_param)
    #FILTERS
    filters_param=read_param.filters()
    print ("filter parameters",filters_param)
    #SAVE
    save_param=read_param.save()
    print ("save parameter",save_param)

#    sys.exit("end of tests")

# read images into numpy arrays
    img_a  = openpiv.tools.imread( file_a )
    img_b  = openpiv.tools.imread( file_b )

#treatment of the raw image  
#!! TODO: dirin automatic, read automatically name of image --> ok ?
#    dirin='/media/HDImage/SMARTEOLE/PIV-Nov2015-TIF/PIV_10ms_000lmin_05deg_z539mm_dt35us_1000im/'
#    img_filoutb='mean_image_10ms_000lmin_05deg_z539mm_1.tif'
    
    img_filouta="mean-img_{0}_0.tif".format(filout)
    img_filoutb="mean-img_{0}_1.tif".format(filout)
    print('image A',img_filouta)
    print('image B',img_filoutb)
    if (image_param.compute_mean[0] == True):
        meanimg_a=filters.ensemble_average_images(dirin,pattern_a,img_filouta)
        meanimg_b=filters.ensemble_average_images(dirin,pattern_b,img_filoutb)
    if (image_param.read_mean[0] == True):
        meanimg_a=io.imread(filouta,as_grey=True)
        meanimg_b=io.imread(filoutb,as_grey=True)
    if (image_param.divide_by_mean[0] == True):
        img_a=filters.divide_image(img_a,meanimg_a)
        img_b=filters.divide_image(img_b,meanimg_b)
    if (image_param.display_mean[0] == True):
        plt.imshow(meanimg_a,clim=(0,1000),cmap=cm.gray)
        plt.show('Mean image A')
        plt.imshow(meanimg_b,clim=(0,1000),cmap=cm.gray)
        plt.show('Mean image B')
        plt.imshow(img_a,clim=(0,1000),cmap=cm.gray)
        plt.show('Divide by mean image A')
        plt.imshow(img_b,clim=(0,1000),cmap=cm.gray)
        plt.show('Divide by mean image B')

# Crop images for faster computations (initial images: identify image.tif 4032*2688 px)
# CROP parameters: 
# !TODO:include crop parameters in parameters.cdl file
    xi=600
    xf=2200 #au lieu de 2688
    yi=0
    yf=1024 #au lieu de 4032
    if image_param.tronc[0]==True:
# Tronc images:
        frame_a=img_a[xi:xf,yi:yf]
        frame_b=img_b[xi:xf,yi:yf]
    else:
        frame_a=img_a
        frame_b=img_b

# process image pair with extended search area piv algorithm.
# standard PIV cross-correlation algorithm:
    u, v, sig2noise = openpiv.process.extended_search_area_piv(frame_a.astype(np.int32),frame_b.astype(np.int32), window_size=piv_param.windowsize[0], overlap=piv_param.overlaping[0], dt=piv_param.dt[0]*(1e-6), search_area_size=piv_param.search_area[0], sig2noise_method='peak2peak')

    # get window centers coordinates
    x, y = openpiv.process.get_coordinates(image_size=frame_a.shape, window_size=piv_param.windowsize[0], overlap=piv_param.overlaping[0])    
    x.shape
    # Scaling 
    x, y, u, v = openpiv.scaling.uniform(x, y, u, v, scaling_factor = piv_param.scaling_factor[0])  

    # histogram
    if (filters_param.show_histogram[0]==True):
    # on u and v signals
        plt.hist(u.ravel(),range=(-50,50),bins=1000) #-4<u<12
        plt.show()
        plt.hist(v.ravel(),range=(-10,10),bins=1000) #-4<v<8
        plt.show()
    # sid2noise signal
        plt.hist(sig2noise.ravel(),range=(0,5),bins=100)
        plt.show()

    # sig2noise filter    
    if (filters_param.s2n[0] == True):    
        u, v, mask_s2n = openpiv.validation.sig2noise_val(u, v, sig2noise, threshold = filters_param.s2n_threshold[0])    
        mask_s2n=mask_s2n*filters_param.s2n_flagnum[0]

    # threshold filter on u and v   
    if (filters_param.threshold[0] == True):    
        u,v,mask_threshold=filters.velocity_threshold(u,v,filters_param.threshold_umin[0],filters_param.threshold_umax[0],filters_param.threshold_vmin[0],filters_param.threshold_vmax[0],filters_param.threshold_flagnum[0])

    # replace using median filter
    if (filters_param.median[0] == True):    
        u,v=filters.replace_by_median(u,v,kernel=filters_param.median_kernel[0],iteration=filters_param.median_iteration[0])
     
    # replace using openPIV software
    if (filters_param.localmean[0] == True):    
        u, v = openpiv.filters.replace_outliers(u, v, method='localmean', max_iter=filters_param.localmean_iteration[0], tol=filters_param.localmean_tolerance[0], kernel_size=filters_param.localmean_kernel[0])

    
   # Apply Mask from external file
    filin='/media/HDImage/SMARTEOLE/MASK/mask_all.txt'
    if image_param.apply_mask[0] == True:
        if image_param.tronc[0]==True:
            print 'IMAGE TRONCATED'
            newframe=xi,xf,yi,yf #TODO: take it from .cdl           
            mask_file=filters.read_mask(image_param.mask_dirname,image_param.mask_filename,image_param.mask_rows2skip[0],newframe,piv_param.windowsize[0],piv_param.overlaping[0])
        else:
            print 'IMAGE NOT TRONCATED'
            newframe=0,0,0,0
            mask_file=filters.read_mask(image_param.mask_dirname,image_param.mask_filename,image_param.mask_rows2skip[0],newframe,piv_param.windowsize[0],piv_param.overlaping[0])

        mask_index=np.where((mask_file == 1)|(mask_file >0))
        mask_file=mask_file*image_param.mask_flagnum[0]
        u[mask_index]=0
        v[mask_index]=0

    # Final flag
    if (filters_param.s2n[0] == False):
        mask_s2n=0
            
    if (filters_param.threshold[0] == False):
        mask_threshold=0
    
    if (image_param.apply_mask[0] == False):
        mask_file=0
        
    final_mask=mask_s2n+mask_threshold+mask_file
    
    # SAVE IN FILE
    temp=counter+1
    if save_param.txt == True:
    # Save to a .txt file 
        openpiv.tools.save(x, y, u, v, final_mask,os.path.join(dirout,'{0}_{1:04d}.txt'.format(filout, temp )),fmt='%8.7f',delimiter='\t')
    if save_param.netcdf_format[0] == True:
    # Save to a .nc file 
        filename=os.path.join(dirout,'{0}_{1:04d}.nc'.format(filout,temp))
        write_NetCDF.PIV2D2C(filename,u,v,x,y,final_mask)


    # DISPLAY
    if save_param.display[0]==True:
        #plot image A (first exposition)
    #        plt.imshow(frame_a,clim=(0,2500),cmap=cm.gray)
        #plot vector field 
#        openpiv.tools.display_vector_field(op.join(dirout,'{0}_{1:04d}.txt'.format(filout,temp)), scale=300, width=0.0025)
        #plot isovalues of u
#        img=plt.imshow(u,interpolation='bicubic',vmin=-10.,vmax=10.)
#        plt.colorbar(img,orientation='horizontal')
        #plot 
        img=plt.imshow(mask_mask_file,interpolation='bicubic',vmin=-1.,vmax=2.)
        plt.colorbar(img,orientation='horizontal')
        plt.show()
        Norm = np.sqrt(u**2+v**2)
        # plot different masks
        ##mask on signal to noise filter:
        us2n=np.ma.array(u,mask=np.logical_not(mask_s2n))
        vs2n=np.ma.array(v,mask=np.logical_not(mask_s2n))
        plt.quiver(x,y,us2n,vs2n,angles='xy', headwidth=4, headlength=6,scale=300,color='black')
        ##TODO: replace by threshold filter
        #um=np.ma.array(u,mask=np.logical_not(mask_threshold mask_median))
        #vm=np.ma.array(v,mask=np.logical_not(mask_median))
        #plt.quiver(x,y,um,vm,angles='xy', headwidth=4, headlength=6,scale=300,color='green')
        ##mask from file:
        imaskfile=np.where(maskfile == 1)
        uf=np.ma.array(u,mask=np.logical_not(maskfile))
        uf[imaskfile] = False
        vf=np.ma.array(v,mask=np.logical_not(maskfile))
        vf[imaskfile] = False
        plt.quiver(x,y,uf,vf,angles='xy', headwidth=4, headlength=6,scale=300,color='red')
        ##TODO: replace median by threshold filter (velocity field without mask from file:)
        unew=np.ma.array(u,mask=(maskfile.astype(bool)|mask_median|mask_s2n))
        vnew=np.ma.array(v,mask=(maskfile.astype(bool)|mask_median|mask_s2n))
        plt.quiver(x,y,unew,vnew,angles='xy', headwidth=4, headlength=6,scale=300,color='blue')
        #qk = quiverkey(Q,0,1,1, r'$1 \frac{m}{s}$', coordinates='data', fontproperties={'weight': 'bold'})        
        plt.show()        
    return;


if __name__ == '__main__':
#    file_a='B00001_0.tif'
#    file_b='B00001_1.tif'
#    file_a='VORTEX_1.tif'
#    file_b='VORTEX_2.tif'
#    file_a='PIV_10ms_000lmin_00deg_00001_0.tif'
#    file_b='PIV_10ms_000lmin_00deg_00001_1.tif'
#    file_a='PIV_10ms_000lmin_00deg_z539mm_00001_0.tif'
#    file_b='PIV_10ms_000lmin_00deg_z539mm_00001_1.tif'
#    file_a='PIV_10ms_220lmin_00deg_z539mm_00001_0.tif'
#    file_b='PIV_10ms_220lmin_00deg_z539mm_00001_1.tif'
    dirin='/media/HDImage/SMARTEOLE/PIV-Nov2015-TIF/PIV_10ms_220lmin_00deg_1000im/'
    file_a=os.path.join(dirin,'B00100_0.tif')
    file_b=os.path.join(dirin,'B00100_1.tif')
#    file_a='PIV_10ms_300lmin_05deg_z539mm_00300_0.tif'
#    file_b='PIV_10ms_300lmin_05deg_z539mm_00300_1.tif'
    dirout='.'
    filout='toto'
    fileparam='parameters.nc'
    counter=0
    args=file_a, file_b,counter
    SinglePair(args,dirin=dirin,filout=filout,fp=fileparam)


#TODO:
# apply mask on images instead of vector field
# to remove noise: spreading of grey level and gaussian filter locally (IA:32x32 pixels for example)
# blur ???




