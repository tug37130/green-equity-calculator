import requests
import pandas as pd
import geopandas as gpd

def fetch_census_data(state_code, county_code):
    # Step 1: Pull data using the Census API
    # Base URL segments for Census API
    host = 'https://api.census.gov/data'
    year = '/2019'
    dataset_acronym = '/acs/acs5/profile'
    g = '?get='
    location = f'&for=tract:*&in=state:{state_code}&in=county:{county_code}'
    variables = ['DP02_0011PE', 'DP02_0068PE', 'DP03_0119PE', 'DP04_0046PE']
    usr_key = "APIKEY"  # Replace with your actual API key

    dfs = []  # List to store DataFrames

    # Loop through variables and make requests
    for variable in variables:
        query_url = f"{host}{year}{dataset_acronym}{g}{variable}{location}&key={usr_key}"
        response = requests.get(query_url)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data[1:], columns=data[0])
            df.set_index('tract', inplace=True)
            dfs.append(df)
        else:
            print(f"Error fetching data for {variable}")

    # Merge all DataFrames on 'tract' column
    merged_df = pd.concat(dfs, axis=1)
    merged_df = merged_df.loc[:,~merged_df.columns.duplicated()]

    # Calculate 'DISAD_INDEX' and create 'GEOID'
    merged_df['DISAD_INDEX'] = ((((merged_df['DP03_0119PE'].astype(float)/10) + (merged_df['DP02_0011PE'].astype(float)/10)) - ((merged_df['DP02_0068PE'].astype(float)/10) + (merged_df['DP04_0046PE'].astype(float)/10)))/4)
    merged_df['GEOID'] = merged_df['state'] + merged_df['county'] + merged_df.index

    # Step 2: Fetch GeoJSON data using the TIGERweb API
    base_url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS2019/MapServer/8/query"
    params = {
        "f": "geojson",
        "where": f"COUNTY='{county_code}' AND STATE='{state_code}'",
        "outFields": "TRACT,GEOID",
        "returnGeometry": True,
        "outSR": 4326
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        geojson_data = response.json()
        if "features" in geojson_data:
            gdf = gpd.GeoDataFrame.from_features(geojson_data)
        else:
            print("No features (tracts) found in the response.")
            return None
    else:
        print("Failed to fetch data from the TIGERweb API.")
        return None

    # Step 3: Merge the DataFrame and GeoDataFrame on 'GEOID'
    final_gdf = gdf.merge(merged_df, on="GEOID")

    return final_gdf

# Example usage:
# state_code = '42'  # Pennsylvania
# county_code = '101'  # Philadelphia County
# final_gdf = fetch_census_data(state_code, county_code)
# print(final_gdf)