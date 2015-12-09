import numpy as np
import gdal
import lad_exceptions
import math

def read_metadata_parameter (metadata_path, parameter):
    metadata_file = open (metadata_path,'r')
    for line in metadata_file:
        if line.find(parameter) <> -1:
            equal_symbol_entrance = line.find ('=')
            value = line [equal_symbol_entrance+1:].replace(' ','').replace('"','')
            return value
    raise lad_exceptions.MetadataError ('Parameter ' + parameter + ' not found at metadata')

def save_nparray_as_raster (nparray, driver_name, cell_type, base_raster_XSize, base_raster_YSize, base_raster_projection, base_raster_transform, out_path):
    cols = base_raster_XSize
    rows = base_raster_YSize
    bands = 1
    dt = cell_type
    driver = gdal.GetDriverByName(driver_name)
    out_data = driver.Create(out_path,cols,rows,bands,dt)
    out_data.SetProjection (base_raster_projection)
    out_data.SetGeoTransform (base_raster_transform)

    out_data.GetRasterBand(1).WriteArray (nparray)


def Landsat8_DN_to_radiance (mode, raster_path, channel_number, metadata_path, output_path = None):
    # mode 0 - generate tiff
    # mode 1 - return np array

    try:
        int(channel_number)
    except:
        raise NameError('Channel number is not correct')
    
    if (int(channel_number)) < 1 or (int(channel_number) > 11):
        raise NameError('Channel number is not correct')
    
    metadata_channel_rad_maximum_str = 'RADIANCE_MAXIMUM_BAND_' + str(channel_number)
    metadata_channel_rad_minimum_str = 'RADIANCE_MINIMUM_BAND_' + str(channel_number)

    metadata_channel_quantize_max_str = 'QUANTIZE_CAL_MAX_BAND_' + str(channel_number)
    metadata_channel_quantize_min_str = 'QUANTIZE_CAL_MIN_BAND_' + str(channel_number)

    rad_maximum = float(read_metadata_parameter(metadata_path, metadata_channel_rad_maximum_str))
    rad_minimum = float(read_metadata_parameter(metadata_path, metadata_channel_rad_minimum_str))
    quantize_maximum = float(read_metadata_parameter(metadata_path, metadata_channel_quantize_max_str))
    quantize_minimum = float(read_metadata_parameter(metadata_path, metadata_channel_quantize_min_str))

    landsat_dn_band = gdal.Open(raster_path)

    landsat_dn_band_array = np.array(landsat_dn_band.GetRasterBand(1).ReadAsArray().astype(np.float32))

    landsat_radiance_band_array = ((rad_maximum - rad_minimum)/(quantize_maximum - quantize_minimum))*(landsat_dn_band_array - quantize_minimum) + rad_minimum

    if mode == 0:
        # Write result
        cols = landsat_dn_band.RasterXSize
        rows = landsat_dn_band.RasterYSize
        cell_type = gdal.GDT_Float32
        driver_name = 'GTiff'
        projection = landsat_dn_band.GetProjection()
        transform = landsat_dn_band.GetGeoTransform()
        save_nparray_as_raster(landsat_radiance_band_array,driver_name,cell_type,cols,rows,projection,transform,output_path)
        return
        #return {"cols":cols,"rows":rows,"cell_type":cell_type,"driver_name":driver_name,"projection":projection,"transform":transform}
    else:
        return landsat_radiance_band_array


def Landsat8_simple_temperature (mode, raster_path, channel_number, metadata_path, output_path=None, base_raster=None):
    # mode 0 - generate tiff
    # mode 1 - return np array

    try:
        int(channel_number)
    except:
        raise NameError('Channel number is not correct')

    if (channel_number < 10) or (channel_number > 11):
        raise NameError('Channel number is not correct')

    landsat_radiance_band_array = Landsat8_DN_to_radiance(1,raster_path,channel_number,metadata_path)
    K1_constant = float(read_metadata_parameter(metadata_path,'K1_CONSTANT_BAND_' + str(channel_number)))
    K2_constant = float(read_metadata_parameter(metadata_path,'K2_CONSTANT_BAND_' + str(channel_number)))

    landsat_temperature_array = (K2_constant / np.log((K1_constant/landsat_radiance_band_array)+1)) - 273.15

    if mode == 0:
        base_raster = gdal.Open(raster_path)
        cols = base_raster.RasterXSize
        rows = base_raster.RasterYSize
        cell_type = gdal.GDT_Float32
        driver_name = 'GTiff'
        projection = base_raster.GetProjection()
        transform = base_raster.GetGeoTransform()
        save_nparray_as_raster(landsat_radiance_band_array,driver_name,cell_type,cols,rows,projection,transform,output_path)
    else:
        return landsat_temperature_array


#print read_metadata_parameter ('E:\Landsat8_urban\Petersburg_24_08_15\LC81850182015236LGN00\LC81850182015236LGN00_MTL.txt','FILE_NAME_BAND_8')
#Landsat8_DN_to_radiance(0,'E:\Landsat8_urban\Petersburg_24_08_15\LC81850182015236LGN00\LC81850182015236LGN00_B4.TIF',4,'E:\Landsat8_urban\Petersburg_24_08_15\LC81850182015236LGN00\LC81850182015236LGN00_MTL.txt','e1.tif')
Landsat8_simple_temperature(0,'E:\Landsat8_urban\Petersburg_24_08_15\LC81850182015236LGN00\LC81850182015236LGN00_B11.TIF',11,'E:\Landsat8_urban\Petersburg_24_08_15\LC81850182015236LGN00\LC81850182015236LGN00_MTL.txt','temp11.tif')
