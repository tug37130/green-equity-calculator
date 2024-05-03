
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import requests
import pandas as pd
import geopandas as gpd
from plant_recommendation import write_txt
from census_requests import fetch_census_data
import os
import rasterio
import geopandas as gpd
import numpy as np
from rasterio.mask import mask
from rasterstats import zonal_stats
from submit_but import submit_button_func
from plot import plot_gdf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function for inputs the number only and limiting length
def numeric_input(text, max_length):
    return (text.isdigit() and len(text) <= max_length) or text == ""

# Function to browse the NLCD tif file
def browse_nlcd_file():
    file_path = filedialog.askopenfilename(filetypes=[("TIF files", "*.tif")])
    nlcd_entry.delete(0, tk.END)
    nlcd_entry.insert(0, file_path)

'''
def browse_nlcd2_file():
    file_path = filedialog.askopenfilename(filetypes=[("TIF files", "*.tif")])
    nlcd2_entry.delete(0, tk.END)
    nlcd2_entry.insert(0, file_path)
'''

# Function to browse the census tract shp/geojson file
def browse_census_tract_file():
    file_path = filedialog.askopenfilename(filetypes=[("Shapefiles", "*.shp")])
    census_tract_entry.delete(0, tk.END)
    census_tract_entry.insert(0, file_path)

# Function for plant recommendation
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

def show_plot(plot):
    # Create a new Toplevel window
    plot_window = tk.Toplevel(window)
    plot_window.title('Plot')

    # Embed the plot in the Toplevel window
    canvas = FigureCanvasTkAgg(plot, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



# Function for submit button
def submit():
    statefp = statefp_entry.get()
    countyfp = countyfp_entry.get()
    shapefile_path = census_tract_entry.get()
    #epsg_code = epsg_entry.get()
    nlcd_file = nlcd_entry.get()
    #nlcd2_file = nlcd2_entry.get()
    
    # output folder
    output_folder = filedialog.askdirectory()
    if output_folder:
       # Generate plant recommendations and write to file in the chosen folder
       write_txt(statefp)
    
       # Show plant recommendations
       display_recommendation()
    
       # Show a message box indicating successful completion
       tk.messagebox.showinfo("Info", "Processing starting. Output files will be saved in {}".format(output_folder))

    final_plot = submit_button_func(statefp, countyfp, nlcd_file, output_folder, shapefile_path)
    tk.messagebox.showinfo("Info", "Processing Completed. Created files 'green_equity_index.shp' and 'PlantRecommendations.txt'")
    
    # Display window of preview map
    show_plot(final_plot)
    


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
'''
######### EPSG
epsg_label = tk.Label(window, text="EPSG Code:")
#epsg_var = tk.StringVar()
epsg_entry = tk.Entry(window, validate="key", validatecommand=(window.register(lambda text: numeric_input(text, 4)), '%P'))
'''
# NLCD
nlcd_label = tk.Label(window, text="NLCD Tree Canopy File:")
nlcd_entry = tk.Entry(window, width=40)
browse_nlcd_button = tk.Button(window, text="Browse", command=browse_nlcd_file)
'''
######### NLCD2
nlcd2_label = tk.Label(window, text="NLCD Impervious TIF File:")
nlcd2_entry = tk.Entry(window, width=40)
browse_nlcd2_button = tk.Button(window, text="Browse", command=browse_nlcd2_file)
'''

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
'''
######## Epsg 
epsg_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
epsg_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky="we")
'''

nlcd_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
nlcd_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2, sticky="we")
browse_nlcd_button.grid(row=3, column=3, padx=5, pady=5)
'''
######## nlcd2
nlcd2_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
nlcd2_entry.grid(row=4, column=1, padx=5, pady=5, columnspan=2, sticky="we")
browse_nlcd2_button.grid(row=4, column=3, padx=5, pady=5)
'''
'''
temp_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
temp_entry.grid(row=5, column=1, padx=5, pady=5, columnspan=2, sticky="we")
browse_temp_button.grid(row=5, column=3, padx=5, pady=5)
'''
census_tract_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
census_tract_entry.grid(row=6, column=1, padx=5, pady=5, columnspan=2, sticky="we")
browse_census_tract_button.grid(row=6, column=3, padx=5, pady=5)

submit_button.grid(row=7, column=1, columnspan=2, padx=5, pady=10)

# Start the GUI event loop
window.mainloop()
