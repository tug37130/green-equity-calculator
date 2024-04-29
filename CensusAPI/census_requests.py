import requests
import pandas as pd
import geopandas as gpd

'''
Created: 01/30/2024
Last Edited: 04/26/24
Author: Dylan Ponticel

Primary Function: fetch_census_data
Parameters: State FIPS code (statefp), County FIPS code (countyfp), (Optional) Census tracts shapefile (shapefile_path)
Expected output: Returns a pandas geodataframe including four census variables and a disadvantage index calculated from the variables.
    DP02_0011PE = Percentage of female-headed households with children
    DP02_0068PE = Percentage of adults 25 years or older with a bachelor's degree or higher
    DP03_0119PE = Percentage of families with incomes below the federal poverty threshold
    DP04_0046PE = Percentage of housing units that are owner occupied
    DISAD_INDEX = (((DP03_0119PE/10) + (DP02_0011PE/10)) - ((DP02_0068PE/10) + (DP04_0046PE/10)))/4)

Notes: Census tract shapefile must be the area defined by the statefp and countyfp. If these values do not match, the function will throw an error.
'''

# Primary function. Mandatory parameters are the statefp and countyfp (FIPS codes).
# Optionally takes a shapefile path.
def fetch_census_data(statefp, countyfp, shapefile_path=None):
    # If a shapefile argument is set, convert the shapefile to a geodataframe
    if shapefile_path:
        gdf = gpd.read_file(shapefile_path)
        # Parse the geodataframe for a column similar to 'GEOID' and rename it to 'GEOID'
        geoid_column = next((col for col in gdf.columns if 'GEOID' in col), None)
        if geoid_column:
            gdf.rename(columns={geoid_column: 'GEOID'}, inplace=True)
        # Error handling if there is no column similar to 'GEOID'    
        else:
            print("Error: GEOID column not found in the shapefile.")
            return None

        # Validate GEOID values. Ensure the GEOID column matches that of the input statefp and countyfp variables
        if not gdf['GEOID'].str.startswith(statefp.zfill(2) + countyfp.zfill(3)).all():
            print("Error: Input state or county code does not match with shapefile GEOID.")
            return None

    # If the GEOID checks out, proceed with fetching data
    # Begin by constructing the base request. This script will always fetch four variables from the 2019 ACS dataset.
    host = 'https://api.census.gov/data'
    year = '/2019'
    dataset_acronym = '/acs/acs5/profile'
    g = '?get='
    location = f'&for=tract:*&in=state:{statefp}&in=county:{countyfp}'
    # DP02_0011PE = Percentage of female-headed households with children
    # DP02_0068PE = Percentage of adults 25 years or older with a bachelor's degree or higher
    # DP03_0119PE = Percentage of families with incomes below the federal poverty threshold
    # DP04_0046PE = Percentage of housing units that are owner occupied
    variables = ['DP02_0011PE', 'DP02_0068PE', 'DP03_0119PE', 'DP04_0046PE']
    usr_key = "be105b6e77cfe811d4458d5070e3eaa163125b6d"

    dfs = []  # List to store dataframes

    # For loop through each requested variable and append it to the empty list
    for variable in variables:
        query_url = f"{host}{year}{dataset_acronym}{g}{variable}{location}&key={usr_key}"
        response = requests.get(query_url)
        if response.status_code == 200:
            data = response.json()
            # Ensure columns and data match
            headers = data[0][:-3]
            values = [row[:-3] for row in data[1:]]
            df = pd.DataFrame(values, columns=headers)
            df['state'] = statefp
            df['county'] = countyfp
            df['tract'] = [row[-1] for row in data[1:]]
            dfs.append(df)
        # If the request for a variable is unsuccessful
        else:
            print(f"Error fetching data for {variable}")

    # Merge the dataframes together
    merged_df = pd.concat(dfs, axis=1)
    # Remove duplicated state/county columns
    merged_df = merged_df.loc[:,~merged_df.columns.duplicated()]
    # Create the DISAD_INDEX (Disadvantage Index) field. The calculation used is sourced from Ross and Mirowski, 2001.
    merged_df['DISAD_INDEX'] = ((((merged_df['DP03_0119PE'].astype(float)/10) + (merged_df['DP02_0011PE'].astype(float)/10)) - ((merged_df['DP02_0068PE'].astype(float)/10) + (merged_df['DP04_0046PE'].astype(float)/10)))/4)
    # Create a GEOID field from the state/county/tract fields. The census data does not pull down with a GEOID field. This can be used for later additions to the resulting table.
    merged_df['GEOID'] = merged_df['state'].astype(str) + merged_df['county'].astype(str) + merged_df['tract'].astype(str)

    # If a shapefile path was not given, request a geojson from the TIGER WEB Rest API for the county and state requested.
    if not shapefile_path:
        base_url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS2019/MapServer/8/query"
        params = {
            "f": "geojson",
            "where": f"COUNTY='{countyfp}' AND STATE='{statefp}'",
            "outFields": "TRACT,GEOID",
            "returnGeometry": True,
            "outSR": 4326
        }
        # Put together the response from the API and make the request
        response = requests.get(base_url, params=params)
        # If pulled successfully, convert the geojson into a geodataframe. This is done so the geometries can be stored locally instead of saved to the user's device.
        if response.status_code == 200:
            geojson_data = response.json()
            gdf = gpd.GeoDataFrame.from_features(geojson_data, crs='EPSG:4326')
        # Error handling if the geojson was not pulled successfully.
        else:
            print("Error fetching GeoJSON data.")
            return None
    # Merge the dataframe with the geodataframe on the GEOID column.
    final_gdf = gdf.merge(merged_df, on='GEOID', how='left')
    # The function returns the final_gdf variable to be used in other parts of the application.
    return final_gdf