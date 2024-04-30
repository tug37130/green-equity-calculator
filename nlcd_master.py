import os
import rasterio
import geopandas as gpd
import numpy as np
from rasterio.mask import mask
from rasterstats import zonal_stats

def raster_clipper(raster, polygon):
    # opens raster input in rasterio
    # pulls geometry from polygon input
    # mask method using these two inputs
    # returns a tuple of the new raster information. 
    raster_opened = rasterio.open(raster)
    geometry = polygon.geometry.values[0]
    clipped_rast, transform = mask(raster_opened, [geometry], crop=True)
    return clipped_rast, transform

def write_clip_copy(input_tuple, output_file):
    # a direct raster file must be used for zonal_stats, which this creates.
    # takes input tuple and writes an output.
    data, transform = input_tuple
    metadata = {
        "driver": "GTiff",
        "height": data.shape[1],
        "width": data.shape[2],
        "count": 1,
        "dtype": data.dtype,
        "crs": "EPSG:5070",
        "transform": transform
    }
    with rasterio.open(output_file, "w", **metadata) as dst:
        dst.write(data)
    print(f"Clipped raster saved to {output_file}")


def nlcd_attacher(raster, poly):
    # inputs a direct raster file, a polygon file
    # runs 'raster_clipper', saves output as 'clip' object
    # reclassifies data in clip as 1-100
    # writes "clip_copy.tif" to save changes and for use in zonal_stats
    # mean value of each poly from raster with zonal_stats
    #   then saved as 'stats' object, a geodataframe 
    # rename as final_gdf and return
    clip = raster_clipper(raster, poly)
    reclassified_data = np.interp(clip[0], (0, 255), (1, 100)).astype(np.uint8)
    clip = (reclassified_data, clip[1])

    write_clip_copy(clip, "clip_copy.tif")
    clip_copy = "clip_copy.tif"

    stats = gpd.GeoDataFrame(zonal_stats(poly, clip_copy, affine=clip[1], stats='mean'))
    #final_gdf = selected_tracts.merge(stats['mean'],  how='left', on='geometry')
    
    final_gdf = poly.join(stats)
    print('NLCD field attached!')
    return final_gdf
    #print(selected_tracts.head(1))
'''
raster = 'C:/1_LUCAS/Application Development/NLCDyesh/yesh data/nlcd_tcc_conus_2021_v2021-4.tif'
polygon = 'C:/1_LUCAS/Application Development/NLCDyesh/yesh data/c16590ca-5adf-4332-aaec-9323b2fa7e7d2020328-1-1jurugw.pr6w.dbf'
epsg_code = '2272'
raster_clipper(raster,polygon,epsg_code)
'''