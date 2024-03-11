# Base URL segments
host = 'https://api.census.gov/data'
year = '/2019'
dataset_acronym = '/acs/acs5/profile'
g = '?get='
# Location argument will need to relate to other application arguments
location = '&for=us:*'

# List of variables to pull
variables = [
    'DP02_0011PE,DP02_0068PE',
    'DP03_0119PE',
    'DP04_0046PE'
]

# API key - replace 'your_api_key' with your actual API key
usr_key = f#place key here in quotations)

# Loop through variables and make API requests
#for i, variable_set in enumerate(variables, start=1):
    # Construct the API request URL for each variable set
#    query_url = f"{host}{year}{dataset_acronym}{g}{variable_set}{location}&key={usr_key}"
    # Use request package to call out to the API
#    response = requests.get(query_url)
#    print(response.text)

responses = {}

# Loop through variables and make API requests
for i, variable_set in enumerate(variables, start=1):
    # Construct the API request URL for each variable set
    query_url = f"{host}{year}{dataset_acronym}{g}{variable_set}{location}&key={usr_key}"
    # Use request package to call out to the API
    response = requests.get(query_url)
    # Store the response in the dictionary with a key
    responses[f'response_{i}'] = response.json()

with open('/input_path_here/census_responses.json', 'w') as json_file:
    json.dump(responses, json_file, indent=4)