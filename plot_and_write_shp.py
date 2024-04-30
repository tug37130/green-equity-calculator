# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 19:17:30 2024

@author: tug03166
"""

def plot_gdf(gdf)

    # Prepare the data
    # ...
    
    # Plot the choropleth map
    gdf.plot(column='green_equity_index_score')
    
    # Add a title and legend
    plt.title('Choropleth Map')
    plt.legend()

    # Show the plot
    final_plot = plt.show()
    
    return final_plot