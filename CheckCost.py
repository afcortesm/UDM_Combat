import os
import sys

# -*- coding: utf-8 -*-
"""
Created on 06/05/2025

@author: A.F. Cortes Moreno
"""
import swmm_api
os.chdir(r"C:\Users\acortesmoreno\Desktop\Test")
os.listdir()
import pandas as pd 


lid_base_costs = {
    'Soakaway': 608,
    'Bio_retention_system': 608,
    'Dry_swale': 103,
    'Extensive_green_roof': 486,
    'Intensive_green_roof': 486,
    'Permeable_pavement': 344,
    'Cistern': 161
    }    

lid_unit_costs = {
    'Soakaway': 1000,
    'Bio_retention_system': 200,
    'Dry_swale': 177,
    'Extensive_green_roof': 25,
    'Intensive_green_roof': 46,
    'Permeable_pavement': 70,
    'Cistern': 100
    } 

lid_types = ['Soakaway',
    'Bio_retention_system',
    'Dry_swale',
    'Extensive_green_roof',
    'Intensive_green_roof',
    'Permeable_pavement',
    'Cistern'    
    ]

solution_run = "S1_strategy_ID_c9b3cad3_gen_100_number_0.inp."

inp_file = swmm_api.read_inp_file(solution_run)

LIDs = inp_file['LID_USAGE']

class LIDUsage:
    def __init__(self, subcatchment, lid, n_replicate, area, width, saturation_init,
                 impervious_portion, route_to_pervious, fn_lid_report, drain_to, from_pervious):
        self.subcatchment = subcatchment
        self.lid = lid
        self.n_replicate = n_replicate
        self.area = area
        self.width = width
        self.saturation_init = saturation_init
        self.impervious_portion = impervious_portion
        self.route_to_pervious = route_to_pervious
        self.fn_lid_report = fn_lid_report
        self.drain_to = drain_to
        self.from_pervious = from_pervious

# Step 1: Convert each LIDUsage instance into a dictionary manually
data_dict = {
    key: {
        'subcatchment': lid_usage.subcatchment,
        'lid': lid_usage.lid,
        'n_replicate': lid_usage.n_replicate,
        'area': lid_usage.area,
        'width': lid_usage.width,
        'saturation_init': lid_usage.saturation_init,
        'impervious_portion': lid_usage.impervious_portion,
        'route_to_pervious': lid_usage.route_to_pervious,
        'fn_lid_report': lid_usage.fn_lid_report,
        'drain_to': lid_usage.drain_to,
        'from_pervious': lid_usage.from_pervious
    }
    for key, lid_usage in LIDs.items()
}

BGIs = pd.DataFrame(columns=['Subcatchment','lid','area','width','impervious_portion'])
rows = []

for key, lid_usage in LIDs.items():
    row = {
        'subcatchment': lid_usage.subcatchment,
        'lid': lid_usage.lid,
        'area': lid_usage.area,
        'width': lid_usage.width,
        'impervious_portion': lid_usage.impervious_portion
        }
    rows.append(row)


# Calculate the cost for each BGI
BGIs['cost'] = BGIs['area'] * BGIs['lid'].map(lid_unit_costs)

# Add the base cost only once for each unique BGI type
unique_lids = BGIs['lid'].unique()  # Get unique BGI types
base_cost_total = sum([lid_base_costs[lid] for lid in unique_lids])

# Calculate the total cost
Tot_Cost = BGIs['cost'].sum() + base_cost_total

print(f"Total Cost: {Tot_Cost}")


import pandas as pd

# Extract the LID_USAGE section from the inp file
lid_usage_data = [
    {
        'subcatchment': lid_usage.subcatchment,
        'lid': lid_usage.lid,
        'n_replicate': lid_usage.n_replicate,
        'area': lid_usage.area,
        'width': lid_usage.width,
        'saturation_init': lid_usage.saturation_init,
        'impervious_portion': lid_usage.impervious_portion,
        'route_to_pervious': lid_usage.route_to_pervious,
        'fn_lid_report': lid_usage.fn_lid_report,
        'drain_to': lid_usage.drain_to,
        'from_pervious': lid_usage.from_pervious
    }
    for lid_usage in LIDs.values()
]

# Convert the data into a DataFrame
lid_usage_df = pd.DataFrame(lid_usage_data)

# Export the DataFrame to an Excel file
lid_usage_df.to_csv("LIDS.csv", index=False)

