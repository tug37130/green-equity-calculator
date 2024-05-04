'''
This script takes the finalized geodataframe and plots it based on the equity score field.
Returns a plotted geodataframe pop-up.
Note this will need to be updated with finalized variables and thresholds.
'''

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import Normalize
from matplotlib import cm
import mapclassify as mc
# This import doesn't seem to work, but the following does
from matplotlib_scalebar.scalebar import ScaleBar
# from matplotlib import ScaleBar

def plot_gdf(gdf, statefp, countyfp):
    # create a empty plot for the choropleth map
    fig, ax = plt.subplots(1, figsize=(8, 8))

    # the number of categories
    n_class = 4

    # Set the color scheme
    cmap = plt.cm.get_cmap('YlGnBu', n_class)

    # This is the field which the choropleth map will be visualized
    field = 'green_equity_index_score'

    # Plot the choropleth map based on the field, this can be changed as needed ('equal_interval', 'quantiles', 'FisherJenks', 'NaturalBreaks')
    # NaturalBreaks probably works best
    gdf.plot(column=field, 
            cmap='YlGnBu', 
            edgecolor='0.5', 
            ax = ax,
            linewidth=0.5,
#                      legend=True, #don't use the legend
            k=n_class, #the number of classes
            scheme='NaturalBreaks')


    # Getting the Natural Breaks bins
    nb = mc.NaturalBreaks(gdf[field].dropna(), k=n_class) # NaturalBreaks, FisherJenks, quantile
    vals = list(nb.bins) # Get interval labels
    vals.insert(0, gdf[field].min())


    # Set the location of the legend (x0, y0, width, height), can be adjusted as needed
    axins = ax.inset_axes([0.2, -0.05, 0.6, 0.03])

    # Create a color bar for the map
    norm = mpl.colors.BoundaryNorm(vals, cmap.N)
    n_cmap = cm.ScalarMappable(norm=norm, cmap=cmap)
    cbar = ax.get_figure().colorbar(n_cmap, 
                                    orientation='horizontal', 
                                    cax=axins,
                                    spacing='proportional',  # Distance in legend proportional to the value
                                    fraction=0.046, 
                                    pad=0.0, 
                                    ticks=vals,
                                    shrink=0.4)

    cbar.ax.set_xlabel('Green Equity Score')

    # Color
    scale2 = ScaleBar(
        dx=1, 
    #     label='Scale 2', 
        location='lower right',
        font_properties={'family':'serif', 'size': 'large'},
    #     color='#b32400', ##b32400
    #     box_color='yellow',
        box_alpha=1  # Transparecy, can change as needed
    )

    ax.add_artist(scale2)
    
    # Set the title of the plot
    title = f"Mapping Green Equity Score of County {countyfp} of State {statefp}"
    ax.set_title(title, fontsize=16, pad=20)


    ax.set_axis_off()
    plt.axis('equal')
    #final_plot = plt.show()

    return plt.gcf()
