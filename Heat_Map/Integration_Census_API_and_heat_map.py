# -*- coding: utf-8 -*-
"""

@author: tur08893
"""
import fiona
import numpy as np
import rasterio
from rasterio.mask import mask
from rasterio.transform import from_bounds
from shapely.geometry import shape
from pystac.extensions.eo import EOExtension as eo
import odc.stac

def get_least_cloud_cover_item(items):
    return min(items, key=lambda item: eo.ext(item).cloud_cover)

def load_temperature_data(selected_item, bands_of_interest, bbox_of_interest):
    data = odc.stac.stac_load(
        [selected_item], bands=bands_of_interest, bbox=bbox_of_interest
    ).isel(time=0)

    band_info = selected_item.assets["lwir"].extra_fields["raster:bands"][0]
    temperature = data["lwir"].astype(float)
    temperature *= band_info["scale"]
    temperature += band_info["offset"]
    
    return temperature - 273.15  # Convert to Celsius
    
def save_raster_data(data, bbox_of_interest, output_file):
    transform = from_bounds(
        *bbox_of_interest, width=data.shape[1], height=data.shape[0]
    )
    crs = rasterio.crs.CRS.from_epsg(4326)

    with rasterio.open(output_file,'w',driver='GTiff',width=data.shape[1],height=data.shape[0],count=1,dtype=data.dtype,crs=crs,transform=transform,) as dst:
        dst.write(data, 1)


def clip_raster(temp_file, final_gdf, out_raster):
    # Extract shapes from the GeoDataFrame
    shapes = [shape(feature['geometry']) for feature in shpfile_gdf.iterfeatures()]

    # Open the source raster file
    with rasterio.open(temp_file) as src:
        out_image, out_transform = mask(src, shapes, crop=True)
        out_meta = src.meta
    # Update metadata for the clipped raster
    out_meta.update({"driver": "GTiff", "height": out_image.shape[1], "width": out_image.shape[2], "compress": 'lzw', "transform": out_transform})
    # Write the clipped raster to the output file
    with rasterio.open(out_raster, "w", **out_meta) as dest:
        dest.write(out_image)

def extract_temp_for_tracts(out_raster, final_gdf):
    temp_dataset = rasterio.open(out_raster)
    
    # Create a new column to store temperature data in the GeoDataFrame
    final_gdf['temp'] = np.nan

    for idx, row in final_gdf.iterrows():
        geom = row.geometry
        shape = [geom]

        outtemp_image, out_transform = rasterio.mask.mask(temp_dataset, shape, crop=True)
        mean_val = float(np.mean(outtemp_image))

        # Update the 'temp' column with mean temperature value
        final_gdf.loc[idx, 'temp'] = mean_val

    return final_gdf

if __name__ == "__main__":

    # Define parameters
    temp_file = 'temp-landsat/temperature.tif'
    out_raster = 'temp-landsat/maskPhily-temp.tif'
    catalog_url = "https://planetarycomputer.microsoft.com/api/stac/v1"
    bbox_of_interest = [-75.28030313034645, 39.867465570687145, -74.9557457320632, 40.137927528193686]
    time_of_interest = "2021-01-01/2021-12-31"
    bands_of_interest = ["lwir"]

    # Connect to the STAC catalog
    catalog = pystac_client.Client.open(
        catalog_url, modifier=planetary_computer.sign_inplace
    )

    # Search for items within the time and area of interest
    items = catalog.search(
        bbox=bbox_of_interest,
        datetime=time_of_interest,
        collections=["landsat-8-l1"],
    )

    # Get the least cloud cover item
    selected_item = get_least_cloud_cover_item(items)

    # Load and process temperature data
    temperature_data = load_temperature_data(selected_item, bands_of_interest, bbox_of_interest)

    # Save temperature data as a GeoTIFF
    save_raster_data(temperature_data, bbox_of_interest, temp_file)

    # Clip temperature raster to the shapefile boundary
    clip_raster(temp_file, final_gdf, out_raster)

    # Extract temperature data for each Census tract in final_gdf
    final_gdf_with_temp = extract_temp_for_tracts(out_raster, final_gdf)

    print("Temperature data extraction and processing completed.")

