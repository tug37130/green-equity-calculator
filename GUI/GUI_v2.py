import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

def browse_nlcd_file():
    file_path = filedialog.askopenfilename(filetypes=[("TIF files", "*.tif")])
    nlcd_entry.delete(0, tk.END)
    nlcd_entry.insert(0, file_path)

def browse_census_tract_file():
    file_path = filedialog.askopenfilename(filetypes=[("Shapefiles", "*.shp"), ("GeoJSON files", "*.geojson")])
    census_tract_entry.delete(0, tk.END)
    census_tract_entry.insert(0, file_path)

# Create the main window
window = tk.Tk()
window.title("Data Input")

# Create widgets
nlcd_label = tk.Label(window, text="NLCD TIF File:")
nlcd_entry = tk.Entry(window, width=40)
browse_nlcd_button = tk.Button(window, text="Browse", command=browse_nlcd_file)

census_tract_label = tk.Label(window, text="Census Tract File:")
census_tract_entry = tk.Entry(window, width=40)
browse_census_tract_button = tk.Button(window, text="Browse", command=browse_census_tract_file)

# Organize widgets in the layout
nlcd_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
nlcd_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2, sticky="we")
browse_nlcd_button.grid(row=0, column=3, padx=5, pady=5)

census_tract_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
census_tract_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky="we")
browse_census_tract_button.grid(row=1, column=3, padx=5, pady=5)

# Start the GUI event loop
window.mainloop()
