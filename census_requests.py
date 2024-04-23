import requests
import pandas as pd
import geopandas as gpd
import io
import os

def fetch_census_data(statefp, countyfp, shapefile_path=None):
    if shapefile_path:
        gdf = gpd.read_file(shapefile_path)
        geoid_column = next((col for col in gdf.columns if 'GEOID' in col), None)
        if geoid_column:
            gdf.rename(columns={geoid_column: 'GEOID'}, inplace=True)
        else:
            print("Error: GEOID column not found in the shapefile.")
            return None

        # Validate GEOID values
        if not gdf['GEOID'].str.startswith(statefp.zfill(2) + countyfp.zfill(3)).all():
            print("Error: Input state or county code does not match with shapefile GEOID.")
            return None

    # If the GEOID checks out, proceed with fetching data
    host = 'https://api.census.gov/data'
    year = '/2019'
    dataset_acronym = '/acs/acs5/profile'
    g = '?get='
    location = f'&for=tract:*&in=state:{statefp}&in=county:{countyfp}'
    variables = ['DP02_0011PE', 'DP02_0068PE', 'DP03_0119PE', 'DP04_0046PE']
    usr_key = "be105b6e77cfe811d4458d5070e3eaa163125b6d"

    dfs = []  # List to store DataFrames

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
        else:
            print(f"Error fetching data for {variable}")

    merged_df = pd.concat(dfs, axis=1)
    merged_df = merged_df.loc[:,~merged_df.columns.duplicated()]
    merged_df['DISAD_INDEX'] = ((((merged_df['DP03_0119PE'].astype(float)/10) + (merged_df['DP02_0011PE'].astype(float)/10)) - ((merged_df['DP02_0068PE'].astype(float)/10) + (merged_df['DP04_0046PE'].astype(float)/10)))/4)
    merged_df['GEOID'] = merged_df['state'].astype(str) + merged_df['county'].astype(str) + merged_df['tract'].astype(str)

    if not shapefile_path:
        # Fetch GeoJSON data if no shapefile is supplied
        base_url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS2019/MapServer/8/query"
        params = {
            "f": "geojson",
            "where": f"COUNTY='{countyfp}' AND STATE='{statefp}'",
            "outFields": "TRACT,GEOID",
            "returnGeometry": True,
            "outSR": 5070
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            geojson_data = response.json()
            gdf = gpd.GeoDataFrame.from_features(geojson_data, crs='EPSG:5070')
        else:
            print("Error fetching GeoJSON data.")
            return None

    final_gdf = gdf.merge(merged_df, on='GEOID', how='left')
    return final_gdf


# statefp = '06'
#countyfp = '101'
#final_gdf = fetch_census_data(statefp, countyfp)
#print(final_gdf)