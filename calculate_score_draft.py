# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 12:41:50 2024

@author: tug03166
"""
# Ultimate score will be 1-100.
# high scores to be interpreted as good

"""
POPULATION VULNERABILITY PART

Census Data
2015-2019 American Community Survey

File_Field
DP02_0087E: Total Population
DP03_0119PE: Percentage of families with incomes below the federal poverty threshold
DP02_0011PE: Percentage of female-headed households with children
DP02_0068PE: Percentage of adults 25 years or older with bachelor's degree or higher
DP04_0046PE: Percentage of housing units that are owner occupied
"""
# The score a census tract recieves should be representative to how vulerable its population is
# Values from census data already in percentages
# ensure weights sum to 1.0

#simulation census data inputs
DP03_0119PE = 30
DP02_0011PE = 41
DP02_0068PE = 25
DP04_0046PE = 12

#some must be inverted
DP03_0119PE_invert = 100 - DP03_0119PE
DP02_0011PE_invert = 100 - DP02_0011PE
DP02_0068PE_invert = 100 - DP02_0068PE

# Equal Weighting
vuln_equal = (
    DP03_0119PE_invert * 0.25 + DP02_0011PE * 0.25 + DP02_0068PE_invert * 0.25 + DP04_0046PE * 0.25
    )

# Ranked Weighting
# most important to least
vuln_ranked = (
    DP03_0119PE_invert * 0.4 + DP02_0011PE * 0.2 + DP02_0068PE_invert * 0.1 + DP04_0046PE * 0.3
    )

# Alternative Weighting
# Poverty and renters are twice as important as others
vuln_alt = (
    DP03_0119PE_invert * 0.333333 + DP02_0011PE * 0.166667 + DP02_0068PE_invert * 0.166667 + DP04_0046PE * 0.333333
    )

#%%
"""
PHYSICAL GREEN PART

NLCD - National Land Cover Database


Greenspace

Impervious Surfaces

Heat Index
"""

#simulation physical data scores
greenspace = 30
imperv = 70
heat = 60

# Equal Weighting
phys_equal = (
    greenspace * 0.333333 + imperv * 0.333333 + heat * 0.333333
    )

# Ranked Weighting
# most important to least
phys_ranked = (
    greenspace * 0.5 + imperv * 0.166667 + heat * 0.333333
    )

# Alternative Weighting
# greenspace is twice as important as imperv and heat
phys_alt = (
    greenspace * 0.5 + imperv * 0.25 + heat * 0.25
    )

#%%
"""
GREEN EQUITY INDEX

The combining of the two parts
"""

#Equal Weighting
green_equity_index_score = (
    vuln * 0.5 + phys * 0.5 
    )
