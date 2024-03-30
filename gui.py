import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import urllib.request
from tkinter import messagebox 
from id_local_species_v3 import write_readme

# Function to browse the NLCD tif file
def browse_nlcd_file():
    file_path = filedialog.askopenfilename(filetypes=[("TIF files", "*.tif")])
    nlcd_entry.delete(0, tk.END)
    nlcd_entry.insert(0, file_path)


# Function to browse the census tract shp/geojson file
def browse_census_tract_file():
    file_path = filedialog.askopenfilename(filetypes=[("Shapefiles", "*.shp"), ("GeoJSON files", "*.geojson")])
    census_tract_entry.delete(0, tk.END)
    census_tract_entry.insert(0, file_path)


# Function for plant recommendation
def display_readme(shapefile_path):
    # Check if readme.txt exists
    if os.path.exists("readme.txt"):
        # Read content from readme.txt
        with open("readme.txt", "r") as f:
            content = f.read()
        
        # Create a new window to display the content
        display_window = tk.Toplevel(window)
        display_window.title("Plant Recommendations")
        
        # Create a text widget to display the content
        text_widget = tk.Text(display_window)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)  # Disable text editing
        text_widget.pack(expand=True, fill="both")

        # The link to download shapefiles
        link_label = tk.Label(display_window, text="Download Shapefiles", fg="blue", cursor="hand2")
        link_label.pack(expand=True, fill="both")
        link_label.bind("<Button-1>", lambda event: download_shapefiles(shapefile_path))  

    else:
        tk.messagebox.showinfo("Info", "No plant recommendations found. Please submit to generate recommendations.")


# Function to download shapefiles
def download_shapefiles(shapefile_path):
    # Select download folder and input file name
    download_path = filedialog.asksaveasfilename(
        initialdir="/", 
        title="Select Download Location", 
        initialfile=os.path.basename(shapefile_path) + ".zip",
        filetypes=[("ZIP files", "*.zip")]
    )
    
    if download_path:
        download_url = f"http://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip"
        #download_url = f"file://{shapefile_path}"
        
        # Download the shapefiles using urllib
        urllib.request.urlretrieve(url=download_url, filename=download_path)


# Function to prompt user to input shapefiles name
def get_shapefile_name(download_dir, shapefile_path):
    shapefile_name = input("Enter the name for the shapefile: ")
    download_url = f"http://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip"
    
    # Download the shapefiles using urllib
    urllib.request.urlretrieve(url=download_url, filename=os.path.join(download_dir, shapefile_name + ".zip"))


# Function for submit button
def submit():
    state_abbr = state_var.get()
    shapefile_path = census_tract_entry.get()
    
    # Write recommendations to readme.txt
    write_readme(state_abbr)
    
    # Display the content of readme.txt
    display_readme(shapefile_path)  


# Create the MAIN window
window = tk.Tk()
window.title("Green Equity Calculator")


# Create widgets
# States 
state_label = tk.Label(window, text="States:")
state_var = tk.StringVar()
state_dropdown = ttk.Combobox(window, textvariable=state_var, values=["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])
state_dropdown.set("AL")  

# NLCD
nlcd_label = tk.Label(window, text="NLCD TIF File:")
nlcd_entry = tk.Entry(window, width=40)
browse_nlcd_button = tk.Button(window, text="Browse", command=browse_nlcd_file)

# Census Tracts
census_tract_label = tk.Label(window, text="Census Tract File:")
census_tract_entry = tk.Entry(window, width=40)
browse_census_tract_button = tk.Button(window, text="Browse", command=browse_census_tract_file)

submit_button = tk.Button(window, text="Submit", command=submit)


# Organize widgets in the layout
state_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
state_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="we")

nlcd_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
nlcd_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky="we")
browse_nlcd_button.grid(row=1, column=3, padx=5, pady=5)

census_tract_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
census_tract_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky="we")
browse_census_tract_button.grid(row=2, column=3, padx=5, pady=5)

submit_button.grid(row=3, column=1, columnspan=2, padx=5, pady=10)


# Start the GUI event loop
window.mainloop()
