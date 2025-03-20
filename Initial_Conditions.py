# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 09:42:13 2025

@author: acortesmoreno
"""

"""
Code to evaluate the initial conditions of the system
"""

# Usefull libraries throuout the  evaluation process

import os
import pyswmm
import pandas as pd
import numpy as np
import swmm_api
import csv


# Define the path to the folder in which the inp and rpt files are stored

path = r"C:\Python\UDM_Battle\To_Evaluate"

os.chdir(path)

# Look for inp files (in this case there should only be one)

files = [f for f in os.listdir(path) if f.endswith('.inp')]

"""
The following lines read the inp file and extract the information of LIDs. In this case the final result should be 0, as there are
no LIDs implemented
"""

inp_file = swmm_api.read_inp_file(files[0])

LIDs = inp_file['LID_USAGE']


if not LIDs: 
    print("There are no LIDs in the inp")
    Tot_cost = 0
    Biodiv = 0

# Create a list to store the variables and add the total cost and biodiversity, which will be 0 for the initial conditions

Results = []

Results.append(Tot_cost)
Results.append(Biodiv)

"""
The following lines read the rpt file and store the variables in the Resutls list
"""

case = files[0]

rpt = case.replace('.inp','.rpt')

rpt_file = swmm_api.read_rpt_file(rpt)

# Look through the rpt file and identify the variables needed for the evaluation

Flood = rpt_file.flow_routing_continuity['Flooding Loss']['Volume_10^6 ltr']

Results.append(Flood)

Evapo = rpt_file.runoff_quantity_continuity['Evaporation Loss']['Depth_mm']

Results.append(Evapo)

WWTP = rpt_file.outfall_loading_summary.loc['WWTP','Total_Volume_10^6 ltr']

Results.append(WWTP)

CSO = rpt_file.outfall_loading_summary.loc['CSO_overflow','Total_Volume_10^6 ltr']

Results.append(CSO)

Mtss = rpt_file.outfall_loading_summary.loc['CSO_overflow','Total_TSS_kg']

Results.append(Mtss)

"""
Once all the results are stored we are going to write a txt saving the variables
"""

column_names = ["Total_Cost","Biodiversity","Flood","Evaporation","Flow_WWTP","CSO","Pollutant_Mass"]

with open("Initial_Parameters.txt", "w") as file: 
    file.write("\t".join(column_names) + "\n")
    file.write("\t".join(map(str,Results)) + "\n")
    
"""
The results for the inital conditions are saved and can be used for the future evaluations
"""
print('\nThis are the initial values for:\nFlooding: {}\nEvaporation: {}\nFlow to the WWTP: {}\nCSO: {}\nMtss: {}'.format(Flood, Evapo, WWTP, CSO, Mtss))    





