import requests
import pandas as pd
import geopandas as gpd

def fetch_census_data(STATEFP, COUNTYFP, shapefile_path=None):
    # Pull data using the Census API
    host = 'https://api.census.gov/data'
    year = '/2019'
    dataset_acronym = '/acs/acs5/profile'
    g = '?get='
    location = f'&for=tract:*&in=state:{STATEFP}&in=county:{COUNTYFP}'
    variables = ['DP02_0011PE', 'DP02_0068PE', 'DP03_0119PE', 'DP04_0046PE']
    usr_key = "API_KEY"  # Replace with API key

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
            df['state'] = [row[-3] for row in data[1:]]
            df['county'] = [row[-2] for row in data[1:]]
            df['tract'] = [row[-1] for row in data[1:]]
            dfs.append(df)
        else:
            print(f"Error fetching data for {variable}")

    merged_df = pd.concat(dfs, axis=1)
    merged_df = merged_df.loc[:,~merged_df.columns.duplicated()]
    merged_df['DISAD_INDEX'] = ((((merged_df['DP03_0119PE'].astype(float)/10) + (merged_df['DP02_0011PE'].astype(float)/10)) - ((merged_df['DP02_0068PE'].astype(float)/10) + (merged_df['DP04_0046PE'].astype(float)/10)))/4)
    merged_df['GEOID'] = merged_df['state'].astype(str) + merged_df['county'].astype(str) + merged_df['tract'].astype(str)

    if shapefile_path:
        # Load shapefile
        gdf = gpd.read_file(shapefile_path)
        # Detect and rename columns if needed
        geoid_column = next((col for col in gdf.columns if 'GEOID' in col), 'GEOID')
        gdf.rename(columns={geoid_column: 'GEOID'}, inplace=True)
        for col, new_name in [('STATEFP', 'state'), ('COUNTYFP', 'county'), ('TRACTCE', 'tract')]:
            original_column = next((c for c in gdf.columns if col in c), None)
            if original_column:
                gdf.rename(columns={original_column: new_name}, inplace=True)
    else:
        # Fetch GeoJSON data if no shapefile is supplied
        base_url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS2019/MapServer/8/query"
        params = {
            "f": "geojson",
            "where": f"COUNTY='{COUNTYFP}' AND STATE='{STATEFP}'",
            "outFields": "TRACT,GEOID",
            "returnGeometry": True,
            "outSR": 4326
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            geojson_data = response.json()
            gdf = gpd.GeoDataFrame.from_features(geojson_data, crs='EPSG:4326')

    if 'GEOID' not in gdf.columns or 'GEOID' not in merged_df.columns:
        print("Error: 'GEOID' column missing in one of the dataframes.")
        return None

    final_gdf = gdf.merge(merged_df, on='GEOID', how='left')
    return final_gdf

# Usage example
STATEFP = '42'  # Pennsylvania
COUNTYFP = '101'  # Philadelphia County
# shapefile_path = "C:/Users/......"
final_gdf = fetch_census_data(STATEFP, COUNTYFP)
# print(final_gdf) # Print to view results (not necessary)