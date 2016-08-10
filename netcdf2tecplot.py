#!/usr/bin/python
# -*- coding: utf-8 -*-
# 18/05/2016
# conversion of netcdf to tecplot
#
#$ python netcdf2tecplot.py -h
#usage: netcdf2tecplot.py [-h] [-di DIRIN] [-fi FILIN] [-fo FILEOUT]
#                         [-zone ZONE]
#
#Netcdf to tecplot format
#
#optional arguments:
#  -h, --help            show this help message and exit
#  -di DIRIN, --dirin DIRIN
#                        Input Image Directory:
#                        '/media/HDImage/SMARTEOLE/VECTORS/OPENPIV/').
#  -fi FILIN, --filin FILIN
#                        Input NetCDF file to be converted:
#                        'VECTOR_10ms_260lmin_05deg_z536mm_dt35us_STAT.nc').
#  -fo FILEOUT, --fileout FILEOUT
#                        Output tecplot file
#                        'VECTOR_10ms_260lmin_05deg_z536mm_dt35us_STAT.dat').
#  -zone ZONE, --zone ZONE
#                        Zone description in tecplot 'z536mm').

from Scientific.IO.NetCDF import NetCDFFile 
#from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os.path
import argparse

# import utilities
import netcdf_tools

# options and arguments
parser = argparse.ArgumentParser(description="Netcdf to tecplot format", epilog="")
parser.add_argument("-di","--dirin", dest="dirin", help="Input Image Directory: '%(default)s').",default="/media/HDImage/SMARTEOLE/VECTORS/OPENPIV/")
parser.add_argument("-fi","--filin", dest="filin", help="Input NetCDF file to be converted: '%(default)s').",default="VECTOR_10ms_260lmin_05deg_z536mm_dt35us_STAT.nc")
parser.add_argument("-fo","--fileout", dest="fileout", help="Output tecplot file  '%(default)s').",default="VECTOR_10ms_260lmin_05deg_z536mm_dt35us_STAT.dat")
parser.add_argument("-z","--zone", dest="zone", help="Zone description in tecplot '%(default)s').",default="z536mm")
args = parser.parse_args()
print(args)


# prepare file before reading
dirin=args.dirin
filin=args.filin
filename=os.path.join(dirin,filin)
# create netcdf_tools object
netcdf_object=netcdf_tools.read_object(filename)
# set variable name to be red and read
data_name=np.array(['xvar','yvar','uavg','vavg','u2avg','v2avg','u3avg','v3avg','u4avg','v4avg','u2nrm','v2nrm','u3nrm','v3nrm','u4nrm','v4nrm']) 
# read variables
data=netcdf_object.read_data(data_name)
# replace nan numbers by 0 (done only for normilized variables of third order)
data=np.nan_to_num(data)
#convert to tecplot
netcdf_object.tecplot(data,data_name,args.fileout,args.zone)
