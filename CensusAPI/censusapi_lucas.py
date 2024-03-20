# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 10:16:00 2024

@author: tug03166
"""

# dictionary for State abbreviation and FIPS code
import json
import requests
states_fips = {
    "AL": "01",
    "AK": "02",
    "AZ": "04",
    "AR": "05",
    "CA": "06",
    "CO": "08",
    "CT": "09",
    "DE": "10",
    "DC": "11",
    "FL": "12",
    "GA": "13",
    "HI": "15",
    "ID": "16",
    "IL": "17",
    "IN": "18",
    "IA": "19",
    "KS": "20",
    "KY": "21",
    "LA": "22",
    "ME": "23",
    "MD": "24",
    "MA": "25",
    "MI": "26",
    "MN": "27",
    "MS": "28",
    "MO": "29",
    "MT": "30",
    "NE": "31",
    "NV": "32",
    "NH": "33",
    "NJ": "34",
    "NM": "35",
    "NY": "36",
    "NC": "37",
    "ND": "38",
    "OH": "39",
    "OK": "40",
    "OR": "41",
    "PA": "42",
    "RI": "44",
    "SC": "45",
    "SD": "46",
    "TN": "47",
    "TX": "48",
    "UT": "49",
    "VT": "50",
    "VA": "51",
    "WA": "53",
    "WV": "54",
    "WI": "55",
    "WY": "56"
}

# input state abb -> fips code


# census api
host = 'https://api.census.gov/data'
year = '2019'
dataset = 'acs/acs5/profile'
base_url = "/".join([host, year, dataset])
predicates = {}
get_vars = [
    'DP02_0011PE,DP02_0068PE',
    'DP03_0119PE',
    'DP04_0046PE'
]
predicates["get"] = ",".join(get_vars)
"for=tract:*"

# Accepting input of state abbreviation
state_abbreviation = input("Enter state abbreviation: ").upper()

# Getting the associated FIPS state numeric code from the dictionary
fips_code = states_fips.get(state_abbreviation)

# Checking if the state abbreviation is valid
if fips_code:
    # If valid, update the "for" predicate with the FIPS code
    predicates["for"] = "state:{}".format(fips_code)
else:
    print("Invalid state abbreviation.")

predicates["key"] = "7f2df7fc9c960f430ba9ff23d2f06738cb406056"
r = requests.get(base_url, params=predicates)


print(r.text)
#print(r.json()[0])

# with open('C:/1_LUCAS/Application Development/CensusAPITesting/census_responses.json', 'w') as json_file:
#    json.dump(responses, json_file, indent=4)

#
# import pandas as pd
# df = pd.DataFrame(columns=col_names, data=r.json()[1:])
