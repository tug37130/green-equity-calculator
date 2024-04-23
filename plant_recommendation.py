# identify where user's study area is.
# if x state = y region 
# from wildflower data dictionary 
def check_state(STATEFP):
    if STATEFP in ["09", "23", "25", "33", "36", "44", "50"]:
        return "Northeast"
    elif STATEFP in ["10", "21", "24", "34", "39", "42", "51", "54"]:
        return "Mid-Atlantic"
    elif STATEFP in ["01", "05", "12", "13", "22", "28", "37", "45", "47"]:
        return "Southeast"
    elif STATEFP in ["17", "18", "20", "19", "26", "27", "29", "31", "38", "46", "55"]:
        return "Midwest"
    elif STATEFP in ["08", "16", "30", "32", "49", "56"]:
        return "Rocky Mountain"
    elif STATEFP in ["04", "35", "40", "48"]:
        return "Southwest"
    elif STATEFP in ["02", "41", "53"]:
        return "Northwest"
    elif STATEFP in ["06"]:
        return "California"
    elif STATEFP in ["15"]:
        return "Hawaii"
    else:
        return "Invalid input. Please input a 2 digits State FIPS code."

# def check_state(state_abbr):
#     if state_abbr in ['CT', 'MA', 'ME', 'NH', 'NY', 'RI', 'VT']:
#         return "Northeast"
#     elif state_abbr in ['DE', 'KY', 'MD', 'NJ', 'OH', 'PA', 'VA', 'WV']:
#         return "Mid-Atlantic"
#     elif state_abbr in ['AL', 'AR', 'FL', 'GA', 'LA', 'MS', 'NC', 'SC', 'TN']:
#         return "Southeast"
#     elif state_abbr in ['IA', 'IL', 'IN', 'KS', 'MI', 'MN', 'MO', 'ND', 'NE', 'SD', 'WI']:
#         return "Midwest"
#     elif state_abbr in ['CO', 'ID', 'MT', 'NV', 'UT', 'WY']:
#         return "Rocky Mountain"
#     elif state_abbr in ['AZ', 'NM', 'OK', 'TX']:
#         return "Southwest"
#     elif state_abbr in ['AK', 'OR', 'WA']:
#         return "Northwest"
#     elif state_abbr in ['CA']:
#         return "California"
#     elif state_abbr in ['HI']:
#         return "Hawaii"
#     else:
#         return "Invalid input. Please select a US State."


# dictionaries based on region
    
# common TREE based on state
def recommended_trees():
    northeast_trees = {
        "Red Maple": "Acer rubrum",
        "Eastern Redbud": "Cercis canadensis",
        "Japanese Zelkova": "Zelkova serrata",
        "London Plane Tree": "Platanus x acerifolia",
        "Honey Locust": "Gleditsia triacanthos"
    }

    mid_atlantic_trees = {
        "American Sweetgum": "Liquidambar styraciflua",
        "Washington Hawthorn": "Crataegus phaenopyrum",
        "American Hornbeam": "Carpinus caroliniana",
        "Japanese Tree Lilac": "Syringa reticulata",
        "Eastern White Pine": "Pinus strobus"
    }

    southeast_trees = {
        "Live Oak": "Quercus virginiana",
        "Crape Myrtle": "Lagerstroemia indica",
        "Southern Magnolia": "Magnolia grandiflora",
        "Loblolly Pine": "Pinus taeda",
        "Cherry Laurel": "Prunus caroliniana"
    }

    midwest_trees = {
        "Northern Red Oak": "Quercus rubra",
        "Tulip Tree": "Liriodendron tulipifera",
        "American Elm": "Ulmus americana",
        "Serviceberry": "Amelanchier spp.",
        "Hackberry": "Celtis occidentalis"
    }

    rocky_mountain_trees = {
        "Colorado Blue Spruce": "Picea pungens",
        "Quaking Aspen": "Populus tremuloides",
        "Ponderosa Pine": "Pinus ponderosa",
        "Rocky Mountain Juniper": "Juniperus scopulorum",
        "Mountain Ash": "Sorbus spp."
    }

    southwest_trees = {
        "Desert Willow": "Chilopsis linearis",
        "Texas Redbud": "Cercis canadensis var. texensis",
        "Palo Verde": "Parkinsonia spp.",
        "Arizona Cypress": "Cupressus arizonica",
        "Mexican Palo Verde": "Parkinsonia aculeata"
    }

    northwest_trees = {
        "Japanese Maple": "Acer palmatum",
        "Douglas Fir": "Pseudotsuga menziesii",
        "Western Red Cedar": "Thuja plicata",
        "Pacific Dogwood": "Cornus nuttallii",
        "Bigleaf Maple": "Acer macrophyllum"
    }

    california_trees = {
        "California Sycamore": "Platanus racemosa",
        "Coast Live Oak": "Quercus agrifolia",
        "Chinese Pistache": "Pistacia chinensis",
        "Jacaranda": "Jacaranda mimosifolia",
        "Southern California Black Walnut": "Juglans californica"
    }

    hawaii_trees = {
    "Koa": "Acacia koa",
    "Ohia Lehua": "Metrosideros polymorpha",
    "Monkeypod": "Samanea saman",
    "Rainbow Shower Tree": "Cassia fistula",
    "Plumeria": "Plumeria spp."
    }

# returns appropriate trees
    return {
        "Northeast": northeast_trees,
        "Mid-Atlantic": mid_atlantic_trees,
        "Southeast": southeast_trees,
        "Midwest": midwest_trees,
        "Rocky Mountain": rocky_mountain_trees,
        "Southwest": southwest_trees,
        "Northwest": northwest_trees,
        "California": california_trees,
        "Hawaii": hawaii_trees
    }


# WETLAND PLANTS
def recommended_wetland_plants():
    northeast_wetland_plants = {
        "Pickerelweed": "Pontederia cordata",
        "Swamp Milkweed": "Asclepias incarnata",
        "Blue Flag Iris": "Iris versicolor",
        "Skunk Cabbage": "Symplocarpus foetidus",
        "Cattail": "Typha spp."
    }

    mid_atlantic_wetland_plants = {
        "Buttonbush": "Cephalanthus occidentalis",
        "Cardinal Flower": "Lobelia cardinalis",
        "Joe-Pye Weed": "Eutrochium spp.",
        "Sensitive Fern": "Onoclea sensibilis",
        "Bog Goldenrod": "Solidago uliginosa"
    }

    southeast_wetland_plants = {
        "Bald Cypress": "Taxodium distichum",
        "Arrow Arum": "Peltandra virginica",
        "Southern Blue Flag": "Iris virginica",
        "Swamp Hibiscus": "Hibiscus coccineus",
        "Water Oak": "Quercus nigra"
    }

    midwest_wetland_plants = {
        "Marsh Marigold": "Caltha palustris",
        "Bluejoint Grass": "Calamagrostis canadensis",
        "Arrowhead": "Sagittaria spp.",
        "Pickerelweed": "Pontederia cordata",
        "Common Reed": "Phragmites australis"
    }

    rocky_mountain_wetland_plants = {
        "Rocky Mountain Iris": "Iris missouriensis",
        "Western Water Hemlock": "Cicuta douglasii",
        "Bog Orchid": "Platanthera spp.",
        "Common Rush": "Juncus effusus",
        "Buckbean": "Menyanthes trifoliata"
    }

    southwest_wetland_plants = {
        "Arizona Sycamore": "Platanus wrightii",
        "Alkali Bulrush": "Schoenoplectus maritimus",
        "Cattail": "Typha spp.",
        "Common Rush": "Juncus spp.",
        "Sawgrass": "Cladium mariscus"
    }

    northwest_wetland_plants = {
        "Douglas Spirea": "Spiraea douglasii",
        "Horsetail": "Equisetum spp.",
        "Skunk Cabbage": "Lysichiton americanus",
        "Watercress": "Nasturtium officinale",
        "Wapato": "Sagittaria latifolia"
    }

    california_wetland_plants = {
        "Marsh Cinquefoil": "Potentilla palustris",
        "Western Blue Flag": "Iris missouriensis",
        "Broadleaf Cattail": "Typha latifolia",
        "California Blackberry": "Rubus ursinus",
        "California Bulrush": "Schoenoplectus californicus"
    }

    hawaii_wetland_plants = {
        "Hawaiian Fern": "Sadleria cyatheoides",
        "Hawaiian Mint": "Stenogyne calaminthoides",
        "Hawaiian Water Lily": "Nymphaea spp.",
        "Kupukupu Fern": "Nephrolepis spp.",
        "Pua Kala": "Argemone glauca"
    }

    return {
        "Northeast": northeast_wetland_plants,
        "Mid-Atlantic": mid_atlantic_wetland_plants,
        "Southeast": southeast_wetland_plants,
        "Midwest": midwest_wetland_plants,
        "Rocky Mountain": rocky_mountain_wetland_plants,
        "Southwest": southwest_wetland_plants,
        "Northwest": northwest_wetland_plants,
        "California": california_wetland_plants,
        "Hawaii": hawaii_wetland_plants
    }

# WILDFLOWERS
def recommended_wildflowers():
    northeast_wildflowers = {
        "Bloodroot": "Sanguinaria canadensis",
        "Trillium": "Trillium spp.",
        "Jack-in-the-Pulpit": "Arisaema triphyllum",
        "Virginia Bluebells": "Mertensia virginica",
        "Woodland Phlox": "Phlox divaricata"
    }

    mid_atlantic_wildflowers = {
        "Mayapple": "Podophyllum peltatum",
        "Virginia Bluebells": "Mertensia virginica",
        "Celandine Poppy": "Stylophorum diphyllum",
        "Cardinal Flower": "Lobelia cardinalis",
        "Wild Columbine": "Aquilegia canadensis"
    }

    southeast_wildflowers = {
        "Carolina Lupine": "Thermopsis villosa",
        "Scarlet Beebalm": "Monarda didyma",
        "Spider Lily": "Hymenocallis spp.",
        "Indian Pink": "Spigelia marilandica",
        "Butterfly Milkweed": "Asclepias tuberosa"
    }

    midwest_wildflowers = {
        "Purple Coneflower": "Echinacea purpurea",
        "Black-eyed Susan": "Rudbeckia hirta",
        "Wild Bergamot": "Monarda fistulosa",
        "Purple Prairie Clover": "Dalea purpurea",
        "Prairie Blazing Star": "Liatris pycnostachya"
    }

    rocky_mountain_wildflowers = {
        "Columbine": "Aquilegia spp.",
        "Blanket Flower": "Gaillardia spp.",
        "Fireweed": "Chamerion angustifolium",
        "Rocky Mountain Penstemon": "Penstemon strictus",
        "Indian Paintbrush": "Castilleja spp."
    }

    southwest_wildflowers = {
        "Mexican Hat": "Ratibida columnifera",
        "Desert Marigold": "Baileya multiradiata",
        "Saguaro Cactus Blossom": "Carnegiea gigantea",
        "Prickly Pear Cactus Blossom": "Opuntia spp.",
        "Orange Globe Mallow": "Sphaeralcea ambigua"
    }

    northwest_wildflowers = {
        "Pacific Bleeding Heart": "Dicentra formosa",
        "Western Trillium": "Trillium ovatum",
        "Oregon Grape": "Mahonia aquifolium",
        "Shooting Star": "Dodecatheon spp.",
        "Western Buttercup": "Ranunculus occidentalis"
    }

    california_wildflowers = {
        "California Poppy": "Eschscholzia californica",
        "California Lilac": "Ceanothus spp.",
        "California Lupine": "Lupinus spp.",
        "Farewell-to-Spring": "Clarkia amoena",
        "Wild Hyacinth": "Dichelostemma capitatum"
    }

    hawaii_wildflowers = {
        "Hawaiian Hibiscus": "Hibiscus brackenridgei",
        "Hawaiian Sunset Vine": "Stictocardia tiliifolia",
        "Hawaiian Lobelia": "Lobelia spp.",
        "Hawaiian Silversword": "Argyroxiphium spp.",
        "Hawaiian Blue Eyed Grass": "Sisyrinchium montanum"
    }

    return {
        "Northeast": northeast_wildflowers,
        "Mid-Atlantic": mid_atlantic_wildflowers,
        "Southeast": southeast_wildflowers,
        "Midwest": midwest_wildflowers,
        "Rocky Mountain": rocky_mountain_wildflowers,
        "Southwest": southwest_wildflowers,
        "Northwest": northwest_wildflowers,
        "California": california_wildflowers,
        "Hawaii": hawaii_wildflowers
    }

########
# actual function to be utilized
def recommended_plants(STATEFP):
    region = check_state(STATEFP)
    if region == "Invalid input. Please select a US State.":
        return region
    
    recommendations = {
        "Region": region,
        "Trees": recommended_trees()[region],
        "Wetland Plants": recommended_wetland_plants()[region],
        "Wildflowers": recommended_wildflowers()[region]
    }
    
    return recommendations

###
# output written to a PlantRecommendation.txt
def write_txt(STATEFP):
    # Call recommended_plants() to get recommendations
    recommendations = recommended_plants(STATEFP)
    
    # Create or open PlantRecommendation.txt in write mode
    with open("PlantRecommendation.txt", "w") as f:
        # Write recommendations to PlantRecommendation.txt
        f.write("Recommended Plants for State FIPS Code {}\n".format(STATEFP))
        f.write("================================\n\n")
        
        f.write("Region: {}\n\n".format(recommendations["Region"]))
        
        f.write("Trees:\n")
        for tree, scientific_name in recommendations["Trees"].items():
            f.write("- {}: {}\n".format(tree, scientific_name))
        f.write("\n")
        
        f.write("Wetland Plants:\n")
        for plant, scientific_name in recommendations["Wetland Plants"].items():
            f.write("- {}: {}\n".format(plant, scientific_name))
        f.write("\n")
        
        f.write("Wildflowers:\n")
        for flower, scientific_name in recommendations["Wildflowers"].items():
            f.write("- {}: {}\n".format(flower, scientific_name))

write_txt("06")

#%%
# delete PlantRecommendation.txt tool
import os

def delete_txt():
    if os.path.exists("PlantRecommendation.txt"):
        os.remove("PlantRecommendation.txt")
        print("PlantRecommendation.txt has been deleted.")
    else:
        print("PlantRecommendation.txt does not exist.")
#%%