from Scientific.IO.NetCDF import NetCDFFile as Dataset
#from netCDF4 import Dataset
import numpy as np

def DATA2D2C(filename,ux_out,uy_out,x_out,y_out):
    """Storage in NetCDF format: 2D2C datas"""
    # open a new netCDF file for writing.
    ncfile = Dataset(filename,'w') 
    # create the x and y dimensions.
    nx,ny=ux_out.shape
    ncfile.createDimension('x',nx)
    ncfile.createDimension('y',ny)
    # create the variable (4 byte integer in this case)
    # first argument is name of variable, second is datatype, third is
    # a tuple with the names of dimensions.
    #data = ncfile.createVariable('data',np.dtype('int32').char,('x','y'))
    xvar = ncfile.createVariable('xvar','d',('x','y'))
    yvar = ncfile.createVariable('yvar','d',('x','y'))
    ux = ncfile.createVariable('ux','d',('x','y'))
    uy = ncfile.createVariable('uy','d',('x','y'))
    # write data to variable.
    xvar[:] = x_out
    yvar[:] = y_out
    ux[:] = ux_out
    uy[:] = uy_out
    # close the file.
    ncfile.close()
    print '*** SUCCESS writing:',filename

def PIV2D2C(filename,ux_out,uy_out,x_out,y_out,flag):
    """Storage in NetCDF format: 2D2C PIV datas with flags"""
    # open a new netCDF file for writing.
    ncfile = Dataset(filename,'w') 
    # create the x and y dimensions.
    nx,ny=ux_out.shape
    ncfile.createDimension('x',nx)
    ncfile.createDimension('y',ny)
    # create the variable (4 byte integer in this case)
    # first argument is name of variable, second is datatype, third is
    # a tuple with the names of dimensions.
    #data = ncfile.createVariable('data',np.dtype('int32').char,('x','y'))
    xvar = ncfile.createVariable('xvar','d',('x','y'))
    yvar = ncfile.createVariable('yvar','d',('x','y'))
    ux = ncfile.createVariable('ux','d',('x','y'))
    uy = ncfile.createVariable('uy','d',('x','y'))
    Flags = ncfile.createVariable('flag','d',('x','y'))
    # write data to variable.
    xvar[:] = x_out
    yvar[:] = y_out
    ux[:] = ux_out
    uy[:] = uy_out
    Flags[:] = flag
    # close the file.
    ncfile.close()
    print '*** SUCCESS writing:',filename

def OPENPIV2D2C(filename,ux_out,uy_out,x_out,y_out,flag1,flag2,flag3):
    """Storage in NetCDF format: 2D2C PIV datas with 3 flags used in OPENPIV"""
    # open a new netCDF file for writing.
    ncfile = Dataset(filename,'w') 
    # create the x and y dimensions.
    nx,ny=ux_out.shape
    ncfile.createDimension('x',nx)
    ncfile.createDimension('y',ny)
    # create the variable (4 byte integer in this case)
    # first argument is name of variable, second is datatype, third is
    # a tuple with the names of dimensions.
    #data = ncfile.createVariable('data',np.dtype('int32').char,('x','y'))
    xvar = ncfile.createVariable('xvar','d',('x','y'))
    yvar = ncfile.createVariable('yvar','d',('x','y'))
    ux = ncfile.createVariable('ux','d',('x','y'))
    uy = ncfile.createVariable('uy','d',('x','y'))
    Flags1 = ncfile.createVariable('flag1','d',('x','y'))
    Flags2 = ncfile.createVariable('flag2','d',('x','y'))
    Flags3 = ncfile.createVariable('flag3','d',('x','y'))
    # write data to variable.
    xvar[:] = x_out
    yvar[:] = y_out
    ux[:] = ux_out
    uy[:] = uy_out
    Flags1[:] = flag1
    Flags2[:] = flag2
    Flags3[:] = flag3
    # close the file.
    ncfile.close()
    print '*** SUCCESS writing:',filename

if __name__ == '__main__':
    # the output array to write will be nx x ny
    nx = 6 
    ny = 12
    # generate grid x,y
    x = np.linspace(0, nx-1,nx )
    y = np.linspace(0, ny-1, ny)
    X,Y = np.meshgrid(y, x)
    flag = np.zeros(nx*ny)
    # create the output data.
    data_out = np.arange(nx*ny) # 1d array
    data_out.shape = (nx,ny) # reshape data
    flag.shape = (nx,ny) # reshape flag
    DATA2D2C('WriteTest_DATA2D2C.nc',data_out,data_out,X,Y)
    PIV2D2C('WriteTest_PIV2D2C.nc',data_out,data_out,X,Y,flag)
    OPENPIV2D2C('WriteTest_OPENPIV.nc',data_out,data_out,X,Y,flag,flag,flag)
