import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import requests
import pandas as pd
import geopandas as gpd
from plant_recommendation import write_txt
from final_heat_map import fetch_census_data, find_least_cloudy_item, load_band_data, get_band_info, convert_temperature, save_temperature_raster, clip_create_mask_layer, extract_temp_write_shapefile
######## NLCD imports
from RasterMaster import raster_clipper
from RasterMaster import write_clip_copy
from RasterMaster import main_func
import os
import rasterio
import geopandas as gpd
import numpy as np
from rasterio.mask import mask
from rasterstats import zonal_stats

# Function for inputs the number only and limiting length
def numeric_input(text, max_length):
    return text.isdigit() and len(text) <= max_length or text == ""

# Function to browse the NLCD tif file
def browse_nlcd_file():
    file_path = filedialog.askopenfilename(filetypes=[("TIF files", "*.tif")])
    nlcd_entry.delete(0, tk.END)
    nlcd_entry.insert(0, file_path)

# Function to browse the temperature tif file
def browse_temp_file():
    file_path = filedialog.askopenfilename(filetypes=[("TIF files", "*.tif")])
    temp_entry.delete(0, tk.END)
    temp_entry.insert(0, file_path)

# Function to browse the census tract shp file
def browse_census_tract_file():
    file_path = filedialog.askopenfilename(filetypes=[("Shapefiles", "*.shp")])
    census_tract_entry.delete(0, tk.END)
    census_tract_entry.insert(0, file_path)

# Function for display plant recommendation
def display_recommendation():
    # Check if PlantRecommendation.txt exists
    if os.path.exists("PlantRecommendation.txt"):
        # Read content from PlantRecommendation.txt
        with open("PlantRecommendation.txt", "r") as f:
            content = f.read()
        
        # Create a new window to display the content
        display_window = tk.Toplevel(window)
        display_window.title("Plant Recommendations")
        
        # Create a text widget to display the content
        text_widget = tk.Text(display_window)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)  # Disable text editing
        text_widget.pack(expand=True, fill="both")
    else:
        tk.messagebox.showinfo("Info", "No plant recommendations found. Please submit to generate recommendations.")

# Function for save .txt output
def write_txt(statefp, output_folder):
    # Call recommended_plants() to get recommendations
    recommendations = recommended_plants(statefp)
    
    # Construct the file path for the PlantRecommendation.txt file in the output folder
    output_file_path = os.path.join(output_folder, "PlantRecommendation.txt")
    
    # Create or open PlantRecommendation.txt in write mode
    with open(output_file_path, "w") as f:
        # Write recommendations to PlantRecommendation.txt
        f.write("Recommended Plants for State FIPS Code {}\n".format(statefp))
        f.write("================================\n\n")
        
        f.write("Region: {}\n\n".format(recommendations["Region"]))
        
        f.write("Trees:\n")
        for tree, scientific_name in recommendations["Trees"].items():
            f.write("- {}: {}\n".format(tree, scientific_name))
        f.write("\n")
        
        f.write("Wetland Plants:\n")
        for plant, scientific_name in recommendations["Wetland Plants"].items():
            f.write("- {}: {}\n".format(plant, scientific_name))
        f.write("\n")
        
        f.write("Wildflowers:\n")
        for flower, scientific_name in recommendations["Wildflowers"].items():
            f.write("- {}: {}\n".format(flower, scientific_name))


# Function for submit button
def submit():
    statefp = statefp_entry.get()
    countyfp = countyfp_entry.get()
    shapefile_path = census_tract_entry.get()

    # Call the fetch_census_data function
    final_gdf, bbox_of_interest = fetch_census_data(statefp, countyfp, shapefile_path)

    # Check if temperature file is provided
    if temp_entry.get():
        # Connect to the STAC catalog and search for items within the time and area of interest
        catalog_url = "https://planetarycomputer.microsoft.com/api/stac/v1"
        collections_of_interest = ["landsat-c2-l2"]
        selected_item = find_least_cloudy_item(catalog_url, bbox_of_interest, time_of_interest, collections_of_interest)

        # Load band data
        bands_of_interest = ["lwir"]
        data = load_band_data(selected_item, bands_of_interest, bbox_of_interest)
        band_name = "lwir"
        band_info = get_band_info(selected_item, band_name)
        celsius_data = convert_temperature(data["lwir"], band_info)

        # Save temperature data as a GeoTIFF
        temp_raster_file = "temperature.tif"
        crs_epsg = 4326  # Assuming EPSG:4326 for the CRS
        save_temperature_raster(temp_raster_file, celsius_data, bbox_of_interest, crs_epsg)

        # Clip temperature raster to the shapefile boundary
        clipped_masked_raster = 'mask-temp.tif'
        clip_create_mask_layer(temp_raster_file, shapefile_path, clipped_masked_raster)

        # Extract temperature data for each Census tract in final_gdf
        output_shp_res = 'tempCensus-tract.shp'
        extract_temp_write_shapefile(clipped_masked_raster, shapefile_path, output_shp_res)

    # Choose a folder to store output files
    output_folder = filedialog.askdirectory()
    if output_folder:
        # Generate plant recommendations and write to file in the chosen folder
        write_txt(statefp, output_folder)

        # Show plant recommendations
        display_recommendation()

        # Show a message box indicating successful completion
        tk.messagebox.showinfo("Info", "Processing complete. Output files saved in {}".format(output_folder))



# Create the MAIN window for user input
window = tk.Tk()
window.title("Green Equity Calculator")

# Create widgets
# Input state fips code
statefp_label = tk.Label(window, text="State FIPS Code (2 digits only):")
statefp_entry = tk.Entry(window, validate="key", validatecommand=(window.register(lambda text: numeric_input(text, 2)), '%P'))

# Input county fips code
countyfp_label = tk.Label(window, text="County FIPS Code (3 digits only):")
countyfp_entry = tk.Entry(window, validate="key", validatecommand=(window.register(lambda text: numeric_input(text, 3)), '%P'))

# NLCD
nlcd_label = tk.Label(window, text="NLCD TIF File:")
nlcd_entry = tk.Entry(window, width=40)
browse_nlcd_button = tk.Button(window, text="Browse", command=browse_nlcd_file)

# Temperature
temp_label = tk.Label(window, text="Temperature TIF File:")
temp_entry = tk.Entry(window, width=40)
browse_temp_button = tk.Button(window, text="Browse", command=browse_temp_file)

# Census Tracts
census_tract_label = tk.Label(window, text="Census Tract File (optional):")
census_tract_entry = tk.Entry(window, width=40)
browse_census_tract_button = tk.Button(window, text="Browse", command=browse_census_tract_file)

submit_button = tk.Button(window, text="Submit", command=submit)

# Organize widgets in the layout
statefp_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
statefp_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2, sticky="we")

countyfp_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
countyfp_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky="we")

nlcd_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
nlcd_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky="we")
browse_nlcd_button.grid(row=2, column=3, padx=5, pady=5)

temp_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
temp_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2, sticky="we")
browse_temp_button.grid(row=3, column=3, padx=5, pady=5)

census_tract_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
census_tract_entry.grid(row=4, column=1, padx=5, pady=5, columnspan=2, sticky="we")
browse_census_tract_button.grid(row=4, column=3, padx=5, pady=5)

submit_button.grid(row=5, column=1, columnspan=2, padx=5, pady=10)

# Start the GUI event loop
window.mainloop()
