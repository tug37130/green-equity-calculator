# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 11:47:15 2024

@author: tug03166
"""
"""
PA state fips 42
phila county fips 101

"""
import os
path = os.getcwd()
print(path)
import rasterio
import fiona
import geopandas as gpd
#%%
# Data upload
nlcd_file = 'nlcd_tcc_conus_2021_v2021-4.tif'
nlcd_dataset = rasterio.open(nlcd_file)
county_shapefile = 'tracts.shp'
county_gdf = gpd.read_file(county_shapefile)

# select tracts by IDing state and county
state_fips = input("Enter the FIPS code of the State: ")
county_fips = input("Enter the FIPS code of the County: ")
# Filter the states GeoDataFrame based on the user input
selected_county = county_gdf[(county_gdf['STATEFP'] == state_fips) & (county_gdf['COUNTYFP'] == county_fips)]

# apply defined geometry to NLCD data
from rasterio.mask import mask
# Extract the geometry of the selected county
clipped_nlcds = []
for index, row in selected_county.iterrows():
    geometry = row['geometry']
    clipped_nlcd, _ = mask(nlcd_dataset, [geometry], crop=True)
    clipped_nlcds.append(clipped_nlcd)
    
"""
IMPORTANT OBJECTS:
selected_county = county gdf from input fips codes
clipped_nlcd = nlcd data from only ^
"""

# PLOTTING
import matplotlib.pyplot as plt
from rasterio.plot import show

# Create a new figure and axis
fig, ax = plt.subplots(figsize=(8, 8))

# Visualize the clipped NLCD data
show(clipped_nlcd, ax=ax, cmap='Greens')

# Add title
ax.set_title('Tree Canopy Cover for {} County'.format(county_fips))
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Show the plot
plt.show()

#%%
""" Next step is to work with the "clipped_nlcd" object.

-reclassify raster file to scored vectors (1-100)
-apply the tract file overlay
-average score per tract
"""

"""
# copy from ARC project
with arcpy.EnvManager(mask="tracts_PHL", scratchWorkspace=r"C:\1_LUCAS\Application Development\NLCDyesh\arc_NLCD\arc_NLCD.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="nlcd_tcc_conus_2021_v2021-4.tif",
        reclass_field="Value",
        remap="0 2.540000 1;2.540000 5.080000 2;5.080000 7.620000 3;7.620000 10.160000 4;10.160000 12.700000 5;12.700000 15.240000 6;15.240000 17.780000 7;17.780000 20.320000 8;20.320000 22.860000 9;22.860000 25.400000 10;25.400000 27.940000 11;27.940000 30.480000 12;30.480000 33.020000 13;33.020000 35.560000 14;35.560000 38.100000 15;38.100000 40.640000 16;40.640000 43.180000 17;43.180000 45.720000 18;45.720000 48.260000 19;48.260000 50.800000 20;50.800000 53.340000 21;53.340000 55.880000 22;55.880000 58.420000 23;58.420000 60.960000 24;60.960000 63.500000 25;63.500000 66.040000 26;66.040000 68.580000 27;68.580000 71.120000 28;71.120000 73.660000 29;73.660000 76.200000 30;76.200000 78.740000 31;78.740000 81.280000 32;81.280000 83.820000 33;83.820000 86.360000 34;86.360000 88.900000 35;88.900000 91.440000 36;91.440000 93.980000 37;93.980000 96.520000 38;96.520000 99.060000 39;99.060000 101.600000 40;101.600000 104.140000 41;104.140000 106.680000 42;106.680000 109.220000 43;109.220000 111.760000 44;111.760000 114.300000 45;114.300000 116.840000 46;116.840000 119.380000 47;119.380000 121.920000 48;121.920000 124.460000 49;124.460000 127 50;127 129.540000 51;129.540000 132.080000 52;132.080000 134.620000 53;134.620000 137.160000 54;137.160000 139.700000 55;139.700000 142.240000 56;142.240000 144.780000 57;144.780000 147.320000 58;147.320000 149.860000 59;149.860000 152.400000 60;152.400000 154.940000 61;154.940000 157.480000 62;157.480000 160.020000 63;160.020000 162.560000 64;162.560000 165.100000 65;165.100000 167.640000 66;167.640000 170.180000 67;170.180000 172.720000 68;172.720000 175.260000 69;175.260000 177.800000 70;177.800000 180.340000 71;180.340000 182.880000 72;182.880000 185.420000 73;185.420000 187.960000 74;187.960000 190.500000 75;190.500000 193.040000 76;193.040000 195.580000 77;195.580000 198.120000 78;198.120000 200.660000 79;200.660000 203.200000 80;203.200000 205.740000 81;205.740000 208.280000 82;208.280000 210.820000 83;210.820000 213.360000 84;213.360000 215.900000 85;215.900000 218.440000 86;218.440000 220.980000 87;220.980000 223.520000 88;223.520000 226.060000 89;226.060000 228.600000 90;228.600000 231.140000 91;231.140000 233.680000 92;233.680000 236.220000 93;236.220000 238.760000 94;238.760000 241.300000 95;241.300000 243.840000 96;243.840000 246.380000 97;246.380000 248.920000 98;248.920000 251.460000 99;251.460000 254 100",
        missing_values="DATA"
    )
    out_raster.save(r"C:\1_LUCAS\Application Development\NLCDyesh\arc_NLCD\arc_NLCD.gdb\Reclass_nlcd2")
"""
# reformat for this script
import imp
import arcpy

# Convert the geometry of the selected county to a raster mask
selected_county_geometry = selected_county.geometry.iloc[0]  # Assuming you're working with a single selected county
arcpy.PolygonToRaster_conversion(in_features=selected_county_geometry, value_field=None, out_rasterdataset="selected_county_mask", cell_assignment="CELL_CENTER", priority_field="NONE", cellsize=None)
# Set the mask environment setting to the raster mask
arcpy.env.mask = "selected_county_mask"

arcpy.env.scratchWorkspace = r path

# Perform the Reclassify operation
reclass_nlcd_canopy = arcpy.sa.Reclassify(
    in_raster= clipped_nlcd,
    reclass_field="VALUE",
    remap="0 2.540000 1;2.540000 5.080000 2;5.080000 7.620000 3;7.620000 10.160000 4;10.160000 12.700000 5;12.700000 15.240000 6;15.240000 17.780000 7;17.780000 20.320000 8;20.320000 22.860000 9;22.860000 25.400000 10;25.400000 27.940000 11;27.940000 30.480000 12;30.480000 33.020000 13;33.020000 35.560000 14;35.560000 38.100000 15;38.100000 40.640000 16;40.640000 43.180000 17;43.180000 45.720000 18;45.720000 48.260000 19;48.260000 50.800000 20;50.800000 53.340000 21;53.340000 55.880000 22;55.880000 58.420000 23;58.420000 60.960000 24;60.960000 63.500000 25;63.500000 66.040000 26;66.040000 68.580000 27;68.580000 71.120000 28;71.120000 73.660000 29;73.660000 76.200000 30;76.200000 78.740000 31;78.740000 81.280000 32;81.280000 83.820000 33;83.820000 86.360000 34;86.360000 88.900000 35;88.900000 91.440000 36;91.440000 93.980000 37;93.980000 96.520000 38;96.520000 99.060000 39;99.060000 101.600000 40;101.600000 104.140000 41;104.140000 106.680000 42;106.680000 109.220000 43;109.220000 111.760000 44;111.760000 114.300000 45;114.300000 116.840000 46;116.840000 119.380000 47;119.380000 121.920000 48;121.920000 124.460000 49;124.460000 127 50;127 129.540000 51;129.540000 132.080000 52;132.080000 134.620000 53;134.620000 137.160000 54;137.160000 139.700000 55;139.700000 142.240000 56;142.240000 144.780000 57;144.780000 147.320000 58;147.320000 149.860000 59;149.860000 152.400000 60;152.400000 154.940000 61;154.940000 157.480000 62;157.480000 160.020000 63;160.020000 162.560000 64;162.560000 165.100000 65;165.100000 167.640000 66;167.640000 170.180000 67;170.180000 172.720000 68;172.720000 175.260000 69;175.260000 177.800000 70;177.800000 180.340000 71;180.340000 182.880000 72;182.880000 185.420000 73;185.420000 187.960000 74;187.960000 190.500000 75;190.500000 193.040000 76;193.040000 195.580000 77;195.580000 198.120000 78;198.120000 200.660000 79;200.660000 203.200000 80;203.200000 205.740000 81;205.740000 208.280000 82;208.280000 210.820000 83;210.820000 213.360000 84;213.360000 215.900000 85;215.900000 218.440000 86;218.440000 220.980000 87;220.980000 223.520000 88;223.520000 226.060000 89;226.060000 228.600000 90;228.600000 231.140000 91;231.140000 233.680000 92;233.680000 236.220000 93;236.220000 238.760000 94;238.760000 241.300000 95;241.300000 243.840000 96;243.840000 246.380000 97;246.380000 248.920000 98;248.920000 251.460000 99;251.460000 254 100",
    missing_values="DATA"
)
#resulting object is reclass_nlcd_canopy 
"""
arcpy aint workin, translate to another method
"""

#%%
"""
RECLASSIFY 'clipped_nlcd'
"""
import numpy as np

# Define the number of classes
num_classes = 100

# Extract the values from the clipped raster
raster_values = clipped_nlcd

# Determine the minimum and maximum values
min_value = np.min(raster_values)
max_value = np.max(raster_values)

# Define the class intervals using equal intervals
class_intervals = np.linspace(min_value, max_value, num_classes + 1)

# Perform reclassification based on the class intervals
reclassified_nlcd = np.digitize(raster_values, class_intervals)

# Now, 'reclassified_nlcd' contains the reclassified raster with 100 classes of equal intervals.

#%%
"""
AVERAGING BY TRACT
calcuate average 'value' of 'reclassified_nlcd' per census tract within 'selected_county'
"""
# Create an empty list to store the average values for each census tract
average_values = []

# Iterate over each census tract polygon geometry in the selected county GeoDataFrame
for index, tract in selected_county.iterrows():
    # Extract the geometry of the census tract
    tract_geometry = tract['geometry']
    
    # Mask the reclassified_nlcd raster with the geometry of the census tract
    masked_nlcd, _ = mask(reclassified_nlcd, [tract_geometry], crop=True)
    
    # Calculate the average value for the masked raster
    average_value = np.nanmean(reclassified_nlcd)  # Use np.nanmean to handle NaN values (if any)
    
    # Store the average value along with the census tract identifier
    average_values.append((selected_county['TRACTCE'], average_value))

# Display the average values for each census tract
for tract_id, avg_value in average_values:
    print(f"Census Tract {tract_id}: Average Value = {avg_value}")

