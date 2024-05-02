# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 21:59:25 2024

@author: tur08893
"""

#import fiona
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

def set_bbox(gdf):
    bbox_values = gdf.total_bounds
    bbox_of_interest = [bbox_values[0], bbox_values[1], bbox_values[2], bbox_values[3]]
    return bbox_of_interest

def find_least_cloudy_item(catalog_url, bbox_of_interest, time_of_interest, collections):
    try:
        # Open the STAC catalog
        catalog = pystac_client.Client.open(
            catalog_url,
            modifier=planetary_computer.sign_inplace,
        )

        # Search for items based on criteria
        search = catalog.search(
            collections=["landsat-c2-l2"],
            bbox=bbox_of_interest,
            datetime=time_of_interest,
            query={
                "eo:cloud_cover": {"lt": 10},
                "platform": {"in": ["landsat-8", "landsat-9"]},
            },
        )
        items = search.get_all_items()
        print(f"Returned {len(items)} Items")
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


# Function to load band data from a selected item using Open Data Cube (ODC)
def load_band_data(selected_item, bands_of_interest, bbox_of_interest):
    # Load data from the selected item with specified bands and bounding box
    data = odc.stac.stac_load(
        [selected_item], bands=bands_of_interest, bbox=bbox_of_interest
    ).isel(time=0)
    return data
    
# Function to get information about a specific band from a selected item
def get_band_info(selected_item, band_name):
    # Extract information about the specified band from the selected item
    band_info = selected_item.assets[band_name].extra_fields["raster:bands"][0]
    return band_info

# Function to convert temperature data based on band information
def convert_temperature(data, band_info):
    temperature = data.astype(float)
    temperature *= band_info["scale"]
    temperature += band_info["offset"]
    celsius_temp = temperature - 273.15
    return celsius_temp

# Function for saving a temperature raster layer to a GeoTIFF file
def save_temperature_raster(temp_raster_file, data_array, bbox, crs_epsg=4326):
    transform = from_bounds(*bbox, width=data_array.shape[1], height=data_array.shape[0])
    crs = rasterio.crs.CRS.from_epsg(crs_epsg)
    # Open a new GeoTIFF file for writing
    with rasterio.open(temp_raster_file, 'w', driver='GTiff',
                       width=data_array.shape[1], height=data_array.shape[0],
                       count=1, dtype=data_array.dtype,
                       crs=crs, transform=transform) as dst:
        dst.write(data_array, 1)

# Clip and create a mask layer from raster layer
def clip_create_mask_layer(temp_raster_file, geodataframe, clipped_masked_raster):
    # Extract geometries from the GeoDataFrame
    shapes = [geom for geom in geodataframe.geometry]
    
     # Open the temp raster dataset
    with rasterio.open(temp_raster_file) as src:
        # Perform masking operation using geometries
        out_image, out_transform = mask(src, shapes, crop=True)
        # Get metadata of the input raster
        out_meta = src.meta
    # Update metadata for the output raster
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "compress": 'lzw',
                     "transform": out_transform})
    # Create a new raster file with masked data
    with rasterio.open(clipped_masked_raster, "w", **out_meta) as dest:
        dest.write(out_image)

# Extracting temperature data from cliped raster layer iterating through each polygon of census tracts

def extract_temp_add_column(inraster, final_gdf):
    # Open the raster dataset
    temp_dataset = rasterio.open(inraster)

    # Initialize an empty list to store temperature values
    temp_values = []

    # Iterate over each row in the GeoDataFrame
    for idx, row in final_gdf.iterrows():
        geom = row['geometry']
        shape = [geom]  # rasterio.mask.mask needs the shape to be in a list

        # Mask the raster using the polygon
        outtemp_image, out_transform = mask(temp_dataset, shape, crop=True)

        # Convert to Celsius using given information
        temperature = outtemp_image.astype(float)
        # Calculate the mean temperature value
        mean_val = float(np.mean(temperature))

        # Append the mean temperature value to the list
        temp_values.append(mean_val)

    # Add a new column 'temp' to the GeoDataFrame and populate it with the temperature values
    final_gdf['temp'] = temp_values

    return final_gdf


# usage
#statefp = "34"
#countyfp = "013"
#final_gdf, bbox_of_interest = fetch_census_data(statefp, countyfp)
# Connect to the STAC catalog and search for items within the time and area of interest

from reprojection import reproject_a_gdf


def write_attach_temp(final_gdf):
    # reproject to 4326
    final_gdf = reproject_a_gdf(final_gdf, 4326)
    
    # get bbox
    bbox_of_interest = set_bbox(final_gdf)
    
    # Connect to the STAC catalog and search for items within the time and area of interest
    catalog_url = "https://planetarycomputer.microsoft.com/api/stac/v1"
    collections_of_interest = ["landsat-c2-l2"]
    time_of_interest = "2021-01-01/2021-12-31"
    selected_item = find_least_cloudy_item(catalog_url, bbox_of_interest, time_of_interest, collections_of_interest)
    # Load and process temperature data
    bands_of_interest = "lwir11"
    data = load_band_data(selected_item, bands_of_interest, bbox_of_interest)
    band_info = get_band_info(selected_item, bands_of_interest)
    celsius_data = convert_temperature(data["lwir11"], band_info)
    # writing raster
    
    crs_epsg = 4326
    # Save temperature raster as a GeoTIFF
    temp_raster_file = "temperature.tif"
    save_temperature_raster(temp_raster_file, celsius_data, bbox_of_interest, crs_epsg)
    # Clip temperature raster to the gdf
    clipped_masked_raster = 'mask.tif'
    clip_create_mask_layer(temp_raster_file, final_gdf, clipped_masked_raster)
    # Extract temperature data for each Census tract using final_gdf
    extract_temp_add_column(clipped_masked_raster, final_gdf)
    final_gdf = extract_temp_add_column(clipped_masked_raster, final_gdf)
    return final_gdf
    '''
    #output path for raster files
    output_path1 = os.path.join(output_folder,temp_raster_file)
    output_path2 = os.path.join(output_folder,clipped_masked_raster)
    '''
'''
# for solo usage testing
st = '42'
ct = '101'
final_gdf = fetch_census_data(st, ct)
final_gdf = write_attach_temp(final_gdf)
print(final_gdf)
'''


