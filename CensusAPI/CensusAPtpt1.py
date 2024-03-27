import requests
import pandas as pd

# Base URL segments
host = 'https://api.census.gov/data'
year = '/2019'
dataset_acronym = '/acs/acs5/profile'
g = '?get='
# Location argument will need to relate to other application arguments
#location = '&for=us:*'
location = '&for=tract:*&in=state:42&in=county:101'

# List of variables to pull
variables = [
    'DP02_0011PE', 
    'DP02_0068PE',
    'DP03_0119PE',
    'DP04_0046PE'
]

# API key - replace 'your_api_key' with your actual API key
usr_key = "be105b6e77cfe811d4458d5070e3eaa163125b6d"

dfs = []  # List to store DataFrames

# Loop through variables and make API requests
for variable in variables:
    # Construct the API request URL for each variable
    query_url = f"{host}{year}{dataset_acronym}{g}{variable}{location}&key={usr_key}"
    # Use request package to call out to the API
    response = requests.get(query_url)
    # Check if the response is successful
    if response.status_code == 200:
        # Convert response to DataFrame
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        # Set tractID as index
        df.set_index('tract', inplace=True)
        # Store DataFrame in the list
        dfs.append(df)
    else:
        print(f"Error fetching data for {variable}")

# Merge all DataFrames on 'tract' column
merged_df = pd.concat(dfs, axis=1)

# Remove duplicate 'state' and 'county' columns
merged_df = merged_df.loc[:,~merged_df.columns.duplicated()]

# Add new column "DISAD_INDEX" and set it to a calculation of the other fields
merged_df['DISAD_INDEX'] = ((((merged_df['DP03_0119PE'].astype(float)/10) + (merged_df['DP02_0011PE'].astype(float)/10)) - ((merged_df['DP02_0068PE'].astype(float)/10) + (merged_df['DP04_0046PE'].astype(float)/10)))/4)

# Print the merged DataFrame
print("Merged DataFrame with DISAD_INDEX:")
print(merged_df)