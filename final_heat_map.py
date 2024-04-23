# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 21:59:25 2024

@author: tur08893
"""

import fiona
import numpy as np
import rasterio
import pystac_client
import requests
import pandas as pd
import geopandas as gpd
import planetary_computer
from rasterio.mask import mask
from rasterio.transform import from_bounds
import odc.stac
import os
from census_requests import fetch_census_data
#%%
# statefp = "42"
# countyfp = "101"

# Call the fetch_census_data function
# final_gdf, bbox_of_interest = fetch_census_data(statefp, countyfp)

def find_least_cloudy_item(catalog_url, bbox, time_range, collections):
    try:
        # Open the STAC catalog
        catalog = pystac_client.Client.open(
            catalog_url,
            modifier=planetary_computer.sign_inplace,
        )
        
        # Search for items based on criteria
        search = catalog.search(
            collections=collections,
            bbox=bbox,
            datetime=time_range,
            query={"eo:cloud_cover": {"lt": 10}},
        )
        
        # Get the item collection
        items = search.item_collection()
        
        if len(items) == 0:
            raise ValueError("No items found matching the criteria.")
        
        # Find the least cloudy item
        selected_item = min(items, key=lambda item: item.properties.get("eo:cloud_cover", float("inf")))
        
        return selected_item
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
#%%
# Connect to the STAC catalog and search for items within the time and area of interest
catalog_url = "https://planetarycomputer.microsoft.com/api/stac/v1"
collections_of_interest = ["landsat-c2-l2"]
time_of_interest = "2021-01-01/2021-12-31"
selected_item = find_least_cloudy_item(catalog_url, bbox_of_interest, time_of_interest, collections_of_interest)

if selected_item:
    print(
        f"Choosing {selected_item.id} from {selected_item.datetime.date()}"
        + f" with {selected_item.properties.get('eo:cloud_cover', 'N/A')}% cloud cover"
    )
#%%
def load_band_data(selected_item, bands_of_interest, bbox_of_interest):
    data = odc.stac.stac_load(
        [selected_item], bands=bands_of_interest, bbox=bbox_of_interest
    ).isel(time=0)
    return data

def get_band_info(selected_item, band_name):
    band_info = selected_item.assets[band_name].extra_fields["raster:bands"][0]
    return band_info

def convert_temperature(data, band_info):
    temperature = data.astype(float)
    temperature *= band_info["scale"]
    temperature += band_info["offset"]
    celsius_temp = temperature - 273.15
    return celsius_temp

# downloading and saving the raster layer
def save_temperature_raster(temp_raster_file, data_array, bbox, crs_epsg=4326):
    transform = from_bounds(*bbox, width=data_array.shape[1], height=data_array.shape[0])
    crs = rasterio.crs.CRS.from_epsg(crs_epsg)

    with rasterio.open(temp_raster_file, 'w', driver='GTiff',
                       width=data_array.shape[1], height=data_array.shape[0],
                       count=1, dtype=data_array.dtype,
                       crs=crs, transform=transform) as dst:
        dst.write(data_array, 1)

# Clip and create a mask layer from raster layer
def clip_create_mask_layer(temp_raster_file, shpfile, clipped_masked_raster):
    with fiona.open(shpfile, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]

    with rasterio.open(temp_raster_file) as src:
        out_image, out_transform = mask(src, shapes, crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "compress": 'lzw',
                     "transform": out_transform})

    with rasterio.open(clipped_masked_raster, "w", **out_meta) as dest:
        dest.write(out_image)

# Extracting temperature data from cliped raster layer iterating through each polygon of census tracts

def extract_temp_write_shapefile(inraster, shpfile, output_shp_res):
    # Open the raster dataset
    temp_dataset = rasterio.open(inraster)

    # Prepare the polygon shapefile and then do the overlay of the raster data and the vector data
    lyr = fiona.open(shpfile)
    schema = lyr.schema
    schema['properties']['temp'] = 'float'

    with fiona.open(output_shp_res, 'w', driver="ESRI Shapefile", crs=lyr.crs, schema=schema) as output:
        for idx, feat in enumerate(lyr):
            props = feat['properties']
            geom = feat['geometry']
            shape = [geom]  # rasterio.mask.mask needs the shape to be in a list

            # Mask the raster using the polygon
            outtemp_image, out_transform = rasterio.mask.mask(temp_dataset, shape, crop=True)

            # Convert to Celsius using given information
            temperature = outtemp_image.astype(float)
            # Calculate the mean temperature value
            mean_val = float(np.mean(temperature))

            # Update the calculated temperature value to the field
            props['temp'] = mean_val
            output.write({'properties': props,
                          'geometry': geom
                          })

#%%
# usage
# statefp = "34"
# countyfp = "013"
# Call the fetch_census_data function
final_gdf, bbox_of_interest = fetch_census_data(statefp, countyfp)
# Load and process temperature data
bands_of_interest = ["lwir"]
data = load_band_data(selected_item, bands_of_interest, bbox_of_interest)
band_name = "lwir"
band_info = get_band_info(selected_item, band_name)
celsius_data = convert_temperature(data["lwir"], band_info)
# Save temperature data as a GeoTFF
temp_raster_file = "temperature.tif"
crs_epsg = 4326  # Assuming EPSG:4326 for the CRS
save_temperature_raster(temp_raster_file, celsius_data, bbox_of_interest, crs_epsg)
# convert final_gdf to shapefile
shpfile = "Census_Tracts_2010.shp"
final_gdf.to_file(shpfile)
# Clip temperature raster to the shapefile boundary
clipped_masked_raster = 'mask.tif'
clip_create_mask_layer(temp_raster_file, shpfile, clipped_masked_raster)
# Extract temperature data for each Census tract in final_gdf
output_shp_res = 'temperature_Census-tract.shp'
extract_temp_write_shapefile(clipped_masked_raster, shpfile, output_shp_res)
output_path1 = os.path.join(output_folder,temp_raster_file)
output_path2 = os.path.join(output_folder,shpfile)
output_path3 = os.path.join(output_folder,clipped_masked_raster)
output_path4 = os.path.join(output_folder,output_shp_res)