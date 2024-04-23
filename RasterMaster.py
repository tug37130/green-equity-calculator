import os
import rasterio
import geopandas as gpd
import numpy as np
from rasterio.mask import mask
from rasterstats import zonal_stats

def raster_clipper(raster, polygon, epsg_code):
    
    if epsg_code == True:
       print('didnt work')
    else:
       print('worked')
    raster_opened = rasterio.open(raster)
    geometry = polygon.geometry.values[0]
    clipped_rast, transform = mask(raster_opened, [geometry], crop=True)
    return clipped_rast, transform

def write_clip_copy(input_tuple, output_file, epsg_code):
    data, transform = input_tuple
    metadata = {
        "driver": "GTiff",
        "height": data.shape[1],
        "width": data.shape[2],
        "count": 1,
        "dtype": data.dtype,
        "crs": f"EPSG:{epsg_code}",
        "transform": transform
    }
    with rasterio.open(output_file, "w", **metadata) as dst:
        dst.write(data)
    print(f"Clipped raster saved to {output_file}")


def main_func(raster, poly, epsg_code):
    
    selected_tracts = poly

    clip = raster_clipper(raster, selected_tracts, epsg_code)
    reclassified_data = np.interp(clip[0], (0, 255), (1, 100)).astype(np.uint8)
    clip = (reclassified_data, clip[1])

    write_clip_copy(clip, "clip_copy.tif", epsg_code)
    clip_copy = "clip_copy.tif"

    stats = gpd.GeoDataFrame(zonal_stats(selected_tracts, clip_copy, affine=clip[1], stats='mean'))
    #final_gdf = selected_tracts.merge(stats['mean'],  how='left', on='geometry')
    
    final_gdf = selected_tracts.join(stats)
    print('Tree canopy data attached!')
    return final_gdf
    #print(selected_tracts.head(1))
'''
raster = 'C:/1_LUCAS/Application Development/NLCDyesh/yesh data/nlcd_tcc_conus_2021_v2021-4.tif'
polygon = 'C:/1_LUCAS/Application Development/NLCDyesh/yesh data/c16590ca-5adf-4332-aaec-9323b2fa7e7d2020328-1-1jurugw.pr6w.dbf'
epsg_code = '2272'
raster_clipper(raster,polygon,epsg_code)
'''