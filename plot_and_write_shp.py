# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 19:17:30 2024

@author: tug03166
"""

def plot_gdf(gdf):

    # Prepare the data
    # ...
    
    # Plot the choropleth map
    gdf.plot(column='green_equity_index_score')
    
    # Add a title and legend
    plt.title('Choropleth Map')
    plt.legend()

    # Show the plot
    final_plot = plt.show()
    
    return final_plot



# Writting final_gdf to harddrive as .shp
import os
def write_gdf_to_shp(gdf, output_folder=None):
    """
    Write a GeoDataFrame to a shapefile.

    Parameters:
        geodataframe (GeoDataFrame): The GeoDataFrame to be written.
        output_filename (str): The filename for the output shapefile.
    """
    os.chdir(output_folder)
    output_filename = 'green_equity_index.shp'
    # If output_folder is provided, construct the full path
    if output_folder:
        output_path = os.path.join(output_folder, output_filename)
    else:
        output_path = output_filename
    # Write GeoDataFrame to shapefile
    gdf.to_file(output_path, driver='ESRI Shapefile')


