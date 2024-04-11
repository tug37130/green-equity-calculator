# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 18:11:25 2024

@author: tug03166
"""
"""
NOTE crs for both files is 5070
"""

import rasterio
import geopandas as gpd
import numpy as np
from rasterio.mask import mask
import matplotlib.pyplot as plt
from rasterio.plot import show
import os
from rasterstats import zonal_stats
from shapely.geometry import mapping
import matplotlib as plt
import pandas as pd
from shapely.geometry import box


path = os.getcwd()
print(path)
#%%
nlcd_file = rasterio.open('nlcd_tcc_conus_2021_v2021-4.tif')


tract_shapefile = 'tracts.shp'
state_fips = input("Enter the FIPS code of the State: ")
county_fips = input("Enter the FIPS code of the County: ")

# Tract Selection
def tract_select(tract_shapefile, state_fips, county_fips):
    tract_gdf = gpd.read_file(tract_shapefile)
    selected_tracts = tract_gdf[(tract_gdf['STATEFP'] == state_fips) & (tract_gdf['COUNTYFP'] == county_fips)]
    return selected_tracts

selected_tracts = tract_select(tract_shapefile, state_fips, county_fips)
print(list(selected_tracts))
# PHL 42 101
"""
Objects from this should be :
    1) nlcd_file - the raster dataset
    2) selected_tracts - gdf of tracts of selected county
"""
#%%
# operational File loading
nlcd_file = rasterio.open('nlcd_tcc_conus_2021_v2021-4.tif')

import CensusAPtpt1
selected_tracts = final_gdf

#%%
# Masking function

def raster_clipper(raster, polygon):
    # Extract the geometry of the polygon
    geometry = polygon.geometry.values[0]
    # Preform mask with raster and geometry of polygon arg
    clipped_rast, transform = mask(raster, [geometry], crop=True)
    return clipped_rast, transform

# Usage:
clip = raster_clipper(nlcd_file, selected_tracts)

# object 'clip' is a tuple that holds   nparray and Affine
    
#%%
# RECLASSIFY
# Reclassify the nparray to a range of 1 to 100
reclassified_data = np.interp(clip[0], (0, 255), (1, 100)).astype(np.uint8)
# replace the nparray, updating clip object
clip = (reclassified_data, clip[1])

#%%
# zonal stats expects files to be input. 
# perhaps we write these files

def write_clip_copy(input_tuple, output_file):
    """
    Write clipped raster data to a GeoTIFF file.
    
    Parameters:
        clip (tuple): A tuple containing the clipped raster data and its transform.
        output_file (str): The name of the output GeoTIFF file.
    """
    # Extract data and transform from clip object
    data, transform = input_tuple

    # Specify the metadata for the output raster file
    metadata = {
        "driver": "GTiff",
        "height": data.shape[1],
        "width": data.shape[2],
        "count": 1,
        "dtype": data.dtype,
        "crs": "EPSG:5070",  # Or use the CRS from the original raster
        "transform": transform
    }

    # Write the clipped raster data to the output file
    with rasterio.open(output_file, "w", **metadata) as dst:
        dst.write(data)

    print(f"Clipped raster saved to {output_file}")

# Usage
write_clip_copy(clip, "clip_copy.tif")
clip_copy = "clip_copy.tif"

#%%
# Now get MEAN value for the tract

stats = gpd.GeoDataFrame(zonal_stats(selected_tracts, clip_copy, affine=clip_copy[1], stats='mean'))
selected_tracts = selected_tracts.join(stats)
#print(selected_tracts.head(1))
#print(selected_tracts.keys())

#%%
#delete the clip_copy.tif
os.remove("clip_copy.tif")