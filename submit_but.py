# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 16:45:19 2024

@author: tug03166
"""
import os
import requests
import pandas as pd
import geopandas as gpd
# plants
from plant_recommendation_folder import write_txt
# census
from census_requests import fetch_census_data
######## NLCD imports
from nlcd_master import raster_clipper, write_clip_copy, nlcd_attacher

import os
import rasterio
import geopandas as gpd
import numpy as np
from rasterio.mask import mask
from rasterstats import zonal_stats
# temperature
from heat_map import *
from write_shp import write_gdf_to_shp
from delete import delete_trash
from index_calculator import calc_score, convert_to_float
from plot import plot_gdf



def submit_button_func(statefp, countyfp, nlcd_file, output_folder, shapefile_path=None):
    
    # Fetch Census data
    final_gdf = fetch_census_data(statefp, countyfp, shapefile_path)
    if final_gdf is not None:
        print(final_gdf) # Print to view results (not necessary)
        
    else:
        # Handle error or display message
        pass
    
    # Tree Canopy data
    final_gdf = nlcd_attacher(nlcd_file, final_gdf)
    print(final_gdf)
    print('NLCD attached.')
    
    # Impervious data
    #final_gdf = nlcd_attacher(nlcd2_file, final_gdf, epsg_code)
    
    # Heat data
    final_gdf = write_attach_temp(final_gdf)
    print(final_gdf)
    print('Temperature Data attached.')
    
    # Calculate Green Equity Index Score
    final_gdf = calc_score(final_gdf)
    print(final_gdf)
    print('Green Equity Index Score calcuated.')
    
    # Plotting
    final_plot = plot_gdf(final_gdf, statefp, countyfp)
    
    # Write .shp
    write_gdf_to_shp(final_gdf, output_folder)
    
    # Delete extra files process wrote
    delete_trash(['clip_copy.tif', 'mask.tif', 'temperature.tif'])
    
    return final_plot
    
