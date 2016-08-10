#!/usr/bin/python
# -*- coding: utf-8 -*-
# 13/01/2015
# OPENPIV
# multiprocesseur
#
#$ncgen -o parameters.nc parameters.cdl;python MultiplePair.py -ncpu 2 -do "/media/HDImage/SMARTEOLE/VECTORS/OPENPIV/PIV_10ms_000lmin_05deg_z539mm_dt35us_1000im/" -fo "VECTOR" -di "/media/HDImage/SMARTEOLE/PIV-Nov2015-TIF/PIV_10ms_000lmin_05deg_z539mm_dt35us_1000im/" -fp "parameters.nc" -pa "B0*_0.tif" -pb "B0*_1.tif"
#
# OR: -pa "B0001?_0.tif" -pb "B0001?_1.tif"
#
#$ python MultiplePair.py -h
#usage: MultiplePair.py [-h] [-ncpu NCPU] [-do DIROUT] [-fo FILOUT]
#                       [-fp PARAMETERS] [-di DIRIN] [-pa PATTERN_A]
#                       [-pb PATTERN_B]
#
#PIV treatment in multiple CPU configuration
#
#optional arguments:
#  -h, --help            show this help message and exit
#  -ncpu NCPU, --ncpu NCPU
#                        : How many CPU ?'2').
#  -do DIROUT, --dirout DIROUT
#                        Output vector field Directory: '.').
#  -fo FILOUT, --filout FILOUT
#                        Output vector field file: 'VECTOR').
#  -fp PARAMETERS, --parameters PARAMETERS
#                        NetCDF file (from .cdl file) that contains PIV
#                        parameters 'parameters.nc').
#  -di DIRIN, --dirin DIRIN
#                        Input Image Directory: '.').
#  -pa PATTERN_A, --patterna PATTERN_A
#                        Pattern first image exposure: 'B0000?_0.tif').
#  -pb PATTERN_B, --patternb PATTERN_B
#                        Pattern second image exposure: 'B0000?_1.tif').
 

import sys
import openpiv.tools
import openpiv.scaling
import openpiv.process
import numpy as np
from io import StringIO
import argparse

import single_pair

# options and arguments
parser = argparse.ArgumentParser(description="PIV treatment in multiple CPU configuration", epilog="")
parser.add_argument("-ncpu","--ncpu", dest="ncpu", help=": How many CPU ?'%(default)s').",default=2)
parser.add_argument("-do","--dirout", dest="dirout", help="Output vector field Directory: '%(default)s').",default=".")
parser.add_argument("-fo","--filout", dest="filout", help="Output vector field file: '%(default)s').",default="VECTOR")
parser.add_argument("-fp","--parameters", dest="parameters", help="NetCDF file (from .cdl file) that contains PIV parameters '%(default)s').",default="parameters.nc")
parser.add_argument("-di","--dirin", dest="dirin", help="Input Image Directory: '%(default)s').",default=".")
parser.add_argument("-pa","--patterna", dest="pattern_a", help="Pattern first image exposure: '%(default)s').",default="B0000?_0.tif")
parser.add_argument("-pb","--patternb", dest="pattern_b", help="Pattern second image exposure: '%(default)s').",default="B0000?_1.tif")
args = parser.parse_args()
print(args)

#funcs = []
#for dirout in [ 'testwrap', 'testbis' ] :
funcstr = 'def Fwrap(args) :\n\tsingle_pair.SinglePair(args,"{0}","{1}","{2}","{3}","{4}","{5}")\n'.format(args.dirin,args.dirout,args.filout,args.parameters,args.pattern_a,args.pattern_b)
#print("test",args.dirout)

#print funcstr
exec(funcstr)
#print Fwrap

#funcs.append(Fwrap)
#print("test",args.dirin)
task = openpiv.tools.Multiprocesser(data_dir = args.dirin, pattern_a=args.pattern_a, pattern_b=args.pattern_b)

#for i in (0,1) :
#task.run(funcs[i], n_cpus=1)
task.run(Fwrap, n_cpus=int(args.ncpu))



