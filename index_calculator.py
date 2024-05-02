# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 19:24:10 2024

@author: tug03166
"""
'''
Each field and what must happen to them: 
    
DP03_0119PE: Percentage of families with incomes below the federal poverty threshold
    invert, so higher scores are desirable
    
DP02_0011PE: Percentage of female-headed households with children
    invert, so higher scores are desirable
    
DP02_0068PE: Percentage of adults 25 years or older with bachelor's degree or higher
    
DP04_0046PE: Percentage of housing units that are owner occupied
    
mean : mean nlcd tree canopy coverage score, 1-100

temp : mean temperature, celsius
    
'''

def convert_to_float(gdf, field):
    # Convert fields to float type
    gdf[field] = gdf[field].astype(float)
    return gdf[field]

def calc_score(gdf):
    # convert to floats
    gdf['DP03_0119PE'] = convert_to_float(gdf,'DP03_0119PE')
    gdf['DP03_0011PE'] = convert_to_float(gdf,'DP02_0011PE')
    gdf['DP03_0068PE'] = convert_to_float(gdf,'DP02_0068PE')
    gdf['DP03_0046PE'] = convert_to_float(gdf,'DP04_0046PE')
    # invert appropriate values
    gdf['DP03_0119PE_invert'] = 100 - gdf['DP03_0119PE']
    gdf['DP02_0011PE_invert'] = 100 - gdf['DP02_0011PE']
    # calulate score evenly weighting all fields
    gdf['green_equity_index_score'] = gdf['DP03_0119PE_invert'] * .16667 + gdf['DP02_0011PE_invert'] * .16667 + gdf['DP02_0068PE'] * .16667 + gdf['DP04_0046PE'] * .16667 + gdf['mean'] * .16667 + gdf['temp'] * .16667
    return gdf



# gdf = gdf.drop(columns=['tmp_category'])
