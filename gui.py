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


# Function to browse the census tract shp file
def browse_census_tract_file():
    file_path = filedialog.askopenfilename(filetypes=[("Shapefiles", "*.shp")])
    census_tract_entry.delete(0, tk.END)
    census_tract_entry.insert(0, file_path)


# Function to display plant recommendation from a file
def display_recommendation(output_folder):
    plant_recommendation_file = os.path.join(output_folder, "PlantRecommendation.txt")
    
    # Check if PlantRecommendation.txt exists
    if os.path.exists(plant_recommendation_file):
        # Read content from PlantRecommendation.txt
        with open(plant_recommendation_file, "r") as f:
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
        
        
# Function to display plot in a new window
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
    """Process user inputs and display results."""
    try:
        # Get input values
        statefp = statefp_entry.get()
        countyfp = countyfp_entry.get()
        nlcd_file = nlcd_entry.get()
        
        # Check if any mandatory fields are empty
        if not (statefp and countyfp and nlcd_file):
            # Display a message box indicating missing mandatory fields
            tk.messagebox.showwarning("Warning", "Please fill in all mandatory inputs: State FIPS Code, County FIPS Code, and NLCD Tree Canopy.")
            return
        
        # Proceed when all mandatory fields are filled
        shapefile_path = census_tract_entry.get()
        output_folder = filedialog.askdirectory(title="Select Folder to Store the Output Files")
        if output_folder:
            write_txt(statefp, output_folder)
            display_recommendation(output_folder)
            tk.messagebox.showinfo("Info", "Processing starting. Output files will be saved in {}".format(output_folder))

            final_plot = submit_button_func(statefp, countyfp, nlcd_file, output_folder, shapefile_path)
            tk.messagebox.showinfo("Info", "Processing Completed. Created files 'green_equity_index.shp' and 'PlantRecommendations.txt'")
            show_plot(final_plot)
    except Exception as e:
        # Display an error message box with details
        tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
    
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
nlcd_label = tk.Label(window, text="NLCD Tree Canopy File:")
nlcd_entry = tk.Entry(window, width=40)
browse_nlcd_button = tk.Button(window, text="Browse", command=browse_nlcd_file)

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

census_tract_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
census_tract_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2, sticky="we")
browse_census_tract_button.grid(row=3, column=3, padx=5, pady=5)

submit_button.grid(row=4, column=1, columnspan=2, padx=5, pady=10)


# Start the GUI event loop
window.mainloop()
