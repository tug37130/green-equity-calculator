import os
import rasterio
import geopandas as gpd
import numpy as np
from rasterio.mask import mask
from rasterstats import zonal_stats

    tract_gdf = gpd.read_file(tract_shapefile)
def raster_clipper(raster, polygon):
    geometry = polygon.geometry.values[0]
    clipped_rast, transform = mask(raster, [geometry], crop=True)
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

    clip = raster_clipper(raster, selected_tracts)
    reclassified_data = np.interp(clip[0], (0, 255), (1, 100)).astype(np.uint8)
    clip = (reclassified_data, clip[1])

    write_clip_copy(clip, "clip_copy.tif")
    clip_copy = "clip_copy.tif"

    stats = gpd.GeoDataFrame(zonal_stats(selected_tracts, clip_copy, affine=clip[1], stats='mean'))
    final_gdf = selected_tracts.join(stats)
    return final_gdf
    #print(selected_tracts.head(1))


