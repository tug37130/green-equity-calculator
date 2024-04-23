# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 10:41:41 2024

@author: tug03166
"""
import rasterio
import geopandas as gpd
from rasterio.warp import calculate_default_transform, reproject
import rasterio
from rasterio.warp import calculate_default_transform, reproject

#%%
def reproject_a_gdf(geopandas_df, epsg_code):
    if 'geometry' not in geopandas_df.columns:
            raise ValueError("Input DataFrame does not have a 'geometry' column.")
    epsg = f'EPSG:{epsg_code}'
    reprojected_df = geopandas_df.to_crs(epsg)

    return reprojected_df

#%%
def reproject_shp(input_shp, output_name, epsg_code):
    gdf = gpd.read_file(input_shp)
    if 'geometry' not in gdf.columns:
            raise ValueError("Input DataFrame does not have a 'geometry' column.")
    epsg = f'EPSG:{epsg_code}'
    reprojected_df = geopandas_df.to_crs(epsg)

    return reprojected_df

#%%
#REPROJECT RASTER
#must reproject with with rasterio
# nlcd currently crs:5070


def reproject_raster(input_raster_file, output_raster_file, epsg_code):
    """
    Reprojects a raster file to EPSG:4326.

    Parameters:
    input_raster_file (str): Path to the input raster file.
    output_raster_file (str): Path to save the reprojected raster file.

    Returns:
    None
    """
    # Open the raster file
    with rasterio.open(input_raster_file) as src:
        # Define the new CRS you want to change to
        dst_crs = f'EPSG:{epsg_code}'

        # Calculate the transform and dimensions for the new CRS
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)

        # Update metadata
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        # Create a new raster file with the updated CRS
        with rasterio.open(output_raster_file, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=rasterio.enums.Resampling.nearest)  # You can choose a different resampling method if needed

#%%
# Example usage:
'''
nlcd_file = 'nlcd_tcc_conus_2021_v2021-4.tif'
output_file = 'raster_reprojected.tif'
epsg_code = '4236'
reproject_raster(nlcd_file, output_file, epsg_code)

#%%
print(gpd.read_file('tracts.shp').crs)

crs = nlcd_file.crs()
print (crs.toProj4())


# should let user choose projection
# should let user name output file
'''
