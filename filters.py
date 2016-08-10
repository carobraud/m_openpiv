#!/usr/bin/env python
# 23 Mars 2016
# Filters for OPENPIV 
# 

from skimage import filters, io
import scipy
from scipy import ndimage    
import pylab as plt
import numpy as np
#from matplotlib import cm
import os.path 

from matplotlib import cm #for suface plot
import matplotlib.pyplot as plt
import openpiv.tools
import openpiv.scaling
import openpiv.process
import glob
import pandas as pd #to read cvs files


def read_mask(dirin,filename,rows2skip,cropmask,windowsize,overlap):
     """A function which read mask from DANTEC SoftWare (mask when pixel=1)  
  
        Parameters
        ----------
	dirin: str
.	        Input directory
	filename: str
.	        name of the mask file (in CVS format)
	row2skip: int
.	        row to skip in filename (remove comments)
	cropmask: 4 tuples (xi,xf,yi,yf=cropmask)
	        x and y values to crop filename
        windowsize: int 
                size of the interogation windows
        overlap: int
                size of the overlaping area 
    """
     # read mask file

     filin=os.path.join(os.path.abspath(dirin),filename)
     print ('mask file is:', filin)
     mask_temp=pd.read_csv(filin, decimal=',',delimiter='\t',skiprows=rows2skip)
     # extract values
     xpix=np.array(mask_temp)[:,0]
     ypix=np.array(mask_temp)[:,1]
     mask=np.array(mask_temp)[:,4]
     
     # Reshape 
     maskear=np.array(mask.T).reshape(xpix.max()+1,ypix.max()+1,order='C')
     maskearflip=maskear[:,::-1].T
     # Crop if required
     xi,xf,yi,yf=cropmask            
     if xi==0 and xf==0 and yi==0 and yf==0:
          newmask=maskearflip
     else:
          newmask=maskearflip[xi:xf,yi:yf]

     # Back to vector field 
     dx=windowsize-overlap
     height, width = newmask.shape
     xdim=(width //dx)
     ydim=(height //dx)
     mask_final = np.average(np.split(np.average(np.split(newmask, xdim , axis=1), axis=-1), ydim , axis=1), axis=-1)
     mask_final=mask_final[0:ydim-1,0:xdim-1]
     
     return mask_final;
     

def ensemble_average_images(dirin,pattern,filout):
     """A function to do an ensemble average of images and a spatial average of this ensemble average 
  
        Parameters
        ----------
	dirin: str
.	        Input directory
	pattern: str
	        Input Pattern images to average
	filout: str
	        Output filename 
    """
     #to be able to read high precision images (e.g. 16bits)
     io.use_plugin('freeimage')

     #im=io.imread("B00001_0.tif",as_grey=True)
     #plt.imshow(im)
     #plt.show()
     #pattern="B0*_0.tif"
     #dirin='/media/HDImage/SMARTEOLE/PIV-Nov2015-TIF/PIV_10ms_000lmin_05deg_z539mm_dt35us_1000im/'
     
     # list automatically the file names 
     list_image=sorted( glob.glob( os.path.join( os.path.abspath(dirin), pattern ) ) )
     # Read this list
     imlist=io.imread_collection(list_image)

#not possible to do the average like this: meanimg=sum(imlist)/len(imlist)
     #plt.imshow(imlist[0],clim=(0,1000),cmap=cm.gray)
     #plt.show() 

     # Accumulation of pixel value in float type (to avoid saturation)
     fimlist=imlist[0].astype(float)
     for i in range(len(imlist)-1):
          fimlist += imlist[i+1].astype(float)
     
     
     #plt.hist(fimlist[0].ravel(),bins=10000,range=(30,5500))
     #plt.show()     

     #mean value with float rounded with np.rint()                    
     meanimg_ens=np.rint(fimlist/len(imlist))
     #convert to integer
     meanimg_int=meanimg_ens.astype(np.uint16)
     #mean spatial value rounded with np.rint()
     meanimg_space=np.rint(np.mean(meanimg_ens))
     #convert to integer
     meanimg_space=meanimg_space.astype(np.uint16)

     # Dimensionless mean value 
     mean_out=(np.rint(meanimg_ens/np.mean(meanimg_ens))).astype(np.uint16)
     #plt.imshow(meanimg,clim=(0,100),cmap=cm.gray)
     #plt.show() 
     #io.imsave(filout,meanimg_int)
     
     # save in a file
     io.imsave(filout,mean_out)
     return  mean_out;

def divide_image(img_inst,meanimg):
     """A function which devise any instantaneous image with  
  
        Parameters
        ----------
	img_inst: uint16
.	        Input instantaneous image
	meanimg: uint16
	        Input mean dimensionless image
     """
     #to avoid dividing by zero
     indexzero=np.where(meanimg==0)          
     fmeanimg=meanimg.astype(float)
     fmeanimg[indexzero]=0.01
     return np.rint(img_inst.astype(float)/fmeanimg).astype(np.uint16);


#def enhance_dynamics()
#plt.hist(im.ravel(),bins=200,range=(0,im.max()))
#plt.hist(im.ravel(),bins=10000,range=(0,1000))

def velocity_threshold(u,v,umin_threshold,umax_threshold,vmin_threshold,vmax_threshold,flagnum):
    """Threshold filter on velocity components (2C)
    
       Parameters
       ----------
       u,v: float
              Input velocity components
       umin_threshold: float
              Minimum Input threshold for u component 
       umax_threshold: float
              Maximum Input threshold for u component 
       vmin_threshold: float
              Minimum Input threshold for v component 
       vmax_threshold: float
              Maximum Input threshold for v component 
       flagnum: int
              Input assigned flag number to values affected by the threshold filter
    """

    # find indexes using threshold filter
    index_u=np.where((u<umin_threshold) | (u>umax_threshold))    
    index_v=np.where((v<vmin_threshold) | (v>vmax_threshold))    
    # invalidate u and v using previous indexes
    u[index_u]='NaN'
    v[index_v]='NaN'
    # create mask for u and v
    mask_thresholdu=np.empty(u.shape)
    mask_thresholdv=np.empty(v.shape)
    # fill mask with previous indexes
    tempflag=1
    mask_thresholdu.fill(0)
    mask_thresholdu[index_u]=tempflag
    mask_thresholdv.fill(0)
    mask_thresholdv[index_v]=tempflag
    # Transform mask to bolean
    flagu=mask_thresholdu >= tempflag
    flagv=mask_thresholdv >= tempflag
    # Bolean operation to regoup threshold from u and v
    mask_threshold=np.asarray(flagu)|np.asarray(flagv)
    # Bolean to integer flag
    mask_threshold=flagnum*mask_threshold
    return u,v,mask_threshold;

def median(u,v,flagnum,kernel=3):
    """Median filter: order values and replace the local value by the median one"""
    # apply median filter
    utemp=scipy.signal.medfilt2d(u, kernel_size=kernel) 
    vtemp=scipy.signal.medfilt2d(v, kernel_size=kernel) 
    # find replaced values
    udif=u-utemp
    vdif=v-vtemp
    # find index of replaced values
    mask_median_index=np.where(abs(udif) > 0)
    # create mask 
    mask_median=np.empty(u.shape)
    mask_median.fill(0)
    mask_median[mask_median_index]=flagnum
    # reapply median filter (is there something simpler ??) 
    u=scipy.signal.medfilt2d(u, kernel_size=kernel)
    v=scipy.signal.medfilt2d(v, kernel_size=kernel)
    return u,v,mask_median

def replace_by_median(u,v,kernel=3,iteration=20):
    """Replace outliers defined by 'NaN' values, using a Median filter"""
    # find indexes of u and v where the value is nan
    index_nan=np.where((np.isnan(u)*1 >0)|(np.isnan(v)*1 >0))     
    for i in range(iteration):#while index_nan: NOT POSSIBLE, NEVER CONVERGE (increase kernel size)
        #print np.size(index_nan)
        # apply median filter
        umedian=scipy.signal.medfilt2d(u, kernel_size=kernel)
        vmedian=scipy.signal.medfilt2d(v, kernel_size=kernel)
        # replace orginal field by median filter for nan
        u[index_nan]=umedian[index_nan]
        v[index_nan]=vmedian[index_nan]
        # recalculate index_nan
        index_nan=np.where((np.isnan(u)*1 >0)|(np.isnan(v)*1 >0))

    return u,v

if __name__ == '__main__':

    imagetreat=False
    read_mean=False
    piv=False
    divide_mean=False
    readmask=True
    
    if (readmask == True):
         dirin="/media/HDImage/SMARTEOLE/MASK"
         filename="big_mask.txt"
         rows2skip=8
         #    xi=600
         #    xf=2200
         #    yi=0
         #    yf=1024
         xi=0
         xf=0
         yi=0
         yf=0
         windowsize=32
         overlap=16
         cropmask=xi,xf,yi,yf            
         
         mask=read_mask(dirin,filename,rows2skip,cropmask,windowsize,overlap)
    #    print mask.shape
         img=plt.imshow(mask,interpolation='bicubic',vmin=-1.,vmax=2.)
         plt.colorbar(img,orientation='horizontal')
         plt.show()

    if (imagetreat == True):
        dirin='/media/HDImage/SMARTEOLE/PIV-Nov2015-TIF/PIV_10ms_000lmin_05deg_z539mm_dt35us_1000im/'
        pattern_a="B0*_0.tif"
        pattern_b="B0*_1.tif"
        filouta='mean_image_10ms_000lmin_05deg_z539mm_0.tif'
        filoutb='mean_image_10ms_000lmin_05deg_z539mm_1.tif'
        if read_mean == False:
             meanimg_a=ensemble_average_images(dirin,pattern_a,filouta)
             meanimg_b=ensemble_average_images(dirin,pattern_b,filoutb)               
             #plt.imshow(meanimg_a,clim=(0,500),cmap=plt.cm.gray)
             #plt.show()
             #        plt.imshow(im,clim=(0,1000),cmap=cm.gray)            
             #        plt.hist(im.ravel(),bins=6500,range=(0,im.max()))
             #        plt.imshow(im,clim=(0,1000),cmap=cm.gray)
             #        plt.hist(im.ravel(),bins=10000,range=(0,1000))
        else:
             meanimg_a=io.imread(filouta,as_grey=True)
             meanimg_b=io.imread(filoutb,as_grey=True)

    if (piv == True):
         file_a='B00001_0.tif'
         file_b='B00001_1.tif'   
    #read images
         img_a  = openpiv.tools.imread( file_a )
         img_b  = openpiv.tools.imread( file_b )
#divide image by dimensionless background
         if(divide_mean == True):
              img_a=divide_image(img_a,meanimg_a)
              img_b=divide_image(img_b,meanimg_b)
    # for piv processing    
         frame_a=img_a
         frame_b=img_b
    #parameters for correlation
         dt=35 #microsec
         windowsize=32
         overlaping=16
         search_area=32
    # compute correlation
         u, v, sig2noise = openpiv.process.extended_search_area_piv(frame_a.astype(np.int32),frame_b.astype(np.int32), window_size=windowsize, overlap=overlaping, dt=dt*(1e-6), search_area_size=search_area, sig2noise_method='peak2peak')
    # get window centers coordinates
         x, y = openpiv.process.get_coordinates(image_size=frame_a.shape, window_size=windowsize, overlap=overlaping)    
        # Scaling 
         x, y, u, v = openpiv.scaling.uniform(x, y, u, v, scaling_factor = 21333)  
    #parameters threshold filter
         umin_threshold=-4. #based on histogramme
         umax_threshold=12. #based on histogramme
         vmin_threshold=-3. #based on histogramme
         vmax_threshold=2. #based on histogramme
         flagnum_threshold=2
         flagnum_median=3
        # threshold filter
         u,v,mask_threshold=velocity_threshold(u,v,umin_threshold,umax_threshold,vmin_threshold,vmax_threshold,flagnum_threshold)
         plt.imshow(u)
         plt.show()
        # Replace by median filter
        #    indexNaN=np.where(mask_threshold > 0)
        #    u[indexNaN], v[indexNaN] = replace_by_median(u[indexNaN], v[indexNaN])
        #    plt.imshow(u)
        #    plt.show()
        # median filter
         u,v,mask_median=median(u,v,flagnum_median)
         plt.imshow(u)
         plt.show()
        
