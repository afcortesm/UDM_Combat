# -*- coding: utf-8 -*-
"""
Created on Mon Jun  02 11:20:00 2025

@author: acortesmoreno
"""

"""
This coode reads the best inp file and exports the result into the desired format

"""

import os 
import pandas as pd
import numpy as np
import shutil
import datetime
import pyswmm
import swmm_api
import csv


os.chdir(r"C:\Users\acortesmoreno\OneDrive - Delft University of Technology\Solutions_UDM\02_Evaluation\06_Best")

    
for inp_file in os.listdir():
    if inp_file.endswith('.inp'):
        inp = swmm_api.read_inp_file(inp_file)
        LIDs = inp['LID_USAGE']
    else:
        continue

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
BGIs = pd.DataFrame(rows) 

# Read both sheets into separate DataFrames
xls = pd.ExcelFile("solutions.xlsx")

df_Areas = xls.parse("LID_Areas", skiprows=2, header=None)
df_Perc = xls.parse("LID_Percentage_Implemented", skiprows=2, header=None)

df_Areas.columns = ["Subcatchments", "Soakaway", "Bio retention system", "Dry swale", 
              "Extensive green roof", "Intensive green roof", "Cistern", "Permeable pavement"]
df_Perc.columns = ["Subcatchments", "Soakaway", "Bio retention system", "Dry swale", 
              "Extensive green roof", "Intensive green roof", "Cistern", "Permeable pavement"]

# Ensure subcatchments match formatting
BGIs['subcatchment'] = BGIs['subcatchment'].astype(str)
df_Areas['Subcatchments'] = df_Areas['Subcatchments'].astype(str)
df_Perc['Subcatchments'] = df_Perc['Subcatchments'].astype(str)

# Create mapping from LID names in BGIs to column names in df_Areas and df_Perc
lid_mapping = {
    "Soakaway": "Soakaway",
    "Bio_retention_system": "Bio retention system",
    "Dry_swale": "Dry swale",
    "Extensive_green_roof": "Extensive green roof",
    "Intensive_green_roof": "Intensive green roof",
    "Cistern": "Cistern",
    "Permeable_pavement": "Permeable pavement"
}

# Fill df_Areas with area values
for _, row in BGIs.iterrows():
    subcatchment = row['subcatchment']
    lid_type = row['lid']
    area = row['area']
    
    if lid_type in lid_mapping:
        df_Areas.loc[df_Areas['Subcatchments'] == subcatchment, lid_mapping[lid_type]] = area

# Fill df_Perc with impervious portion values
for _, row in BGIs.iterrows():
    subcatchment = row['subcatchment']
    lid_type = row['lid']
    impervious_portion = row['impervious_portion']
    
    if lid_type in lid_mapping:
        df_Perc.loc[df_Perc['Subcatchments'] == subcatchment, lid_mapping[lid_type]] = impervious_portion

df_Areas.fillna(0, inplace=True)
df_Perc.fillna(0, inplace=True)

df_Areas.to_csv("Areas.csv")
df_Perc.to_csv("Perc.csv")
BGIs.to_csv("BGIs.csv")

sub_implemented = BGIs['subcatchment']
sub_existing = df_Areas['Subcatchments']

