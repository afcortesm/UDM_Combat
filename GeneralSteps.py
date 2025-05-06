# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 12:00:27 2025

@author: acortesmoreno
"""

"""
First test of the code for the Evaluation of results for the UDM Battle - Retrofitting LIDs (BGIs) into Drainage Systems
"""

import os
import pyswmm
import pandas as pd
import numpy as np
import swmm_api
import csv

os.chdir(r"C:\Python\UDM_Battle\Tests")

"""
First, we just read the precipitation and the temperature files and create pandas to store them
They will be use later in the sensibility analysis
"""

rain_data = pd.read_csv("rain2018.dat", delimiter=r"\s+", header=None, names=['Station','Year','Month',"Day",'Hour','Minute',"Value"])
temp_data = pd.read_csv("temp2018.dat", delimiter=r"\s+", header=None, names=['Station','Year','Month',"Day",'Hour','Minute',"Value"])

rain_data['Date'] = pd.to_datetime(rain_data[["Year","Month","Day","Hour","Minute"]],format='%YYYY%mm%d %H:%M')
temp_data['Date'] = pd.to_datetime(temp_data[["Year","Month","Day","Hour","Minute"]],format='%YYYY%mm%d %H:%M')

rain_data = rain_data[["Date","Value"]]
temp_data = temp_data[["Date","Value"]]

rain_data.set_index('Date',inplace=True)
temp_data.set_index('Date',inplace=True)


"""
Choose the inp file to be tested
"""

solution_run = "Case_study_20241121.inp"

inp_file = swmm_api.read_inp_file(solution_run)

LIDs = inp_file['LID_USAGE']

with pyswmm.Simulation(solution_run) as sim:
    start_time = sim.start_time
    end_time = sim.end_time
    total_duration = (end_time - start_time).total_seconds()
    
    print("Simulation Start Time:", start_time)
    print("Simulation End Time:", end_time)
    print("Running Simulation...\n")

    for step in sim:
        # Calculate progress percentage
        current_time = sim.current_time
        elapsed_time = (current_time - start_time).total_seconds()
        progress = (elapsed_time / total_duration) * 100

        # Print progress
        print(f"Progress: {progress:.2f}% ", end="\r")

    print("\nSimulation Completed!")
    



"""
Create a data frame from the LIDs in the inp
"""

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
BGIs = pd.DataFrame(rows)    

"""
Add a column with the cost, multiplying by fixed costs and using the area
"""

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


 

Biodiversity = BGIs.groupby('lid')['area'].sum()

Bio_results = {lid: Biodiversity.get(lid, 0) for lid in lid_types}

min_bio = min(Biodiversity(0), Biodiversity(1), Biodiversity(2), Biodiversity(3))
  
"""
Check out and rpt files
"""

out_file = swmm_api.read_out_file("Case_study_20241121.out")
rpt_file = swmm_api.read_rpt_file("Case_study_20241121.rpt")

Flood = rpt_file.flow_routing_continuity['Flooding Loss']['Volume_10^6 ltr']
Evapo = rpt_file.runoff_quantity_continuity['Evaporation Loss']['Depth_mm']
WWTP = rpt_file.outfall_loading_summary.loc['WWTP','Total_Volume_10^6 ltr']
CSO = rpt_file.outfall_loading_summary.loc['CSO_overflow','Total_Volume_10^6 ltr']
Mtss = rpt_file.outfall_loading_summary.loc['CSO_overflow','Total_TSS_kg']

print('\nThis are the initial values for:\nFlooding: {}\nEvaporation: {}\nFlow to the WWTP: {}\nCSO: {}\nMtss: {}'.format(Flood, Evapo, WWTP, CSO, Mtss))

"""
Create a txt file for every inp and save the final results
"""

            



""" 
Code to read several inp and run all of them
"""

folder_path = r"C:\Python\UDM_Battle\Tests"

inp_files = [f for f in os.listdir(folder_path) if f.endswith('.inp')]

for inp_file in inp_files:
    inp_path = os.path.join(folder_path, inp_file)
    
    print(f"Running Simulation: {inp_file}")
    
    with pyswmm.Simulation(inp_path) as sim:
        for step in sim: 
            current_time = sim.current_time
            elapsed_time = (current_time - start_time).total_seconds()
            progress = (elapsed_time / total_duration) * 100
            print(f"Progress: {progress:.2f}% ", end="\r")
        print("\nSimulation {inp_file} completed :)")
        

"""
Output analysis for sensibility
Remember the time step - every minute
"""

       
#total_area = 70.3446


Flood_series = out_file.get_part('system','', 'flooding')*60/(1e6)
WWTP_series= out_file.get_part('node','WWTP','total_inflow')*60/(1e6)
CSO_series = out_file.get_part('node','CSO_overflow','total_inflow')*60/(1e6)
Evapo_series = out_file.get_part('system','','evaporation')/(24*60)
Pollutant_series = out_file.get_part('node','CSO_overflow','TSS')*CSO_series


Flood_cummulative = Flood_series.cumsum()
Flood_influence = Flood_cummulative/Flood
Flood_inf = Flood_series/Flood


WWTP_cummulative = WWTP_series.cumsum()
WWTP_influence = WWTP_cummulative/WWTP
WWTP_inf = WWTP_series/WWTP


CSO_cummulative = CSO_series.cumsum()
CSO_influence = CSO_cummulative/CSO
CSO_inf = CSO_series/CSO


Evapo_cummulative = Evapo_series.cumsum()
Evapo_influence = Evapo_cummulative/Evapo
Evapo_inf = Evapo_series/Evapo


Pollutant_cummulative = Pollutant_series.cumsum()
Pollutant_influence = Pollutant_cummulative/Mtss
Pollutant_inf = Pollutant_series/Mtss


import matplotlib.pyplot as plt
plt.figure(figsize=(10,5))
plt.ion()

"""
Plot 1 - based on accumulation
"""

plt.plot()

plt.plot(Flood_influence.index, Flood_influence, label='Flood')
plt.plot(WWTP_influence.index, WWTP_influence, label='WWTP')
plt.plot(CSO_influence.index, CSO_influence, label='CSO')
plt.plot(Evapo_influence.index, Evapo_influence, label='Evaporation')
plt.plot(Pollutant_influence.index, Pollutant_influence, label='Pollutant')


plt.xlabel('Date')
plt.ylabel('Influence on final value')
plt.title('Sensibility analysis for variables - accumulation')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

"""
Plot 2 - non accumulation
"""

plt.plot()

plt.plot(Flood_inf.index, Flood_inf, label='Flood')
plt.plot(WWTP_inf.index, WWTP_inf, label='WWTP')
plt.plot(CSO_inf.index, CSO_inf, label='CSO')
plt.plot(Evapo_inf.index, Evapo_inf, label='Evaporation')
plt.plot(Pollutant_inf.index, Pollutant_inf, label='Pollutant')

plt.yscale('log')
plt.xlabel('Date')
plt.ylabel('Influence on final value')
plt.title('Sensibility analysis for variables - non accumulation')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
       





"""
Create the result files
"""

code = os.path.splitext(solution_run)[0]

Eval = [code, Tot_Cost, min_bio, Flood, Evapo, WWTP, CSO, Mtss]

Evaluation_results = []

Evaluation_results.append(Eval)

"""

with open('matrix.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    existing_data = list(reader)

# Append the new rows to the existing data
existing_data.extend(new_rows)

# Rewrite the CSV file with the updated data
with open('matrix.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(existing_data)

print("New rows appended and matrix rewritten to 'matrix.csv'")

"""

"""
Topsis
"""

from topsis import topsis

#Read the CSV or whatever were we are storing the avaialble data and create
#a Pandas

df = Evaluation_results.DataFrame()
#Use the first column as name

weights = [0.1, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1]
impacts = ['-', '+', '+', '+', '+', '+', '+']

df['TOPSIS Score'], df['Rank'] = topsis(df.iloc[:, 1:].values, weights, impacts)
df = df.sort_values(by='Rank')

base_variables = [0, 0, Flood, Evapo, WWTP, CSO, Mtss]



x = 'file.inp'

x_new = x.replace('.inp', '.out')

print(x_new)  


#df = pd.read_csv("Initial_Parameters.txt", sep="\t")

"""
Variables obtained with different time periods
"""

#01/05 until 01/11

r1 = [0,0,0.297,60.814,219.931,43.808,0]
r1_m = [0,0,0.297,60.814,219.931,43.808,3482.625]

from datetime import datetime

date_1 = "2018-05-01"
date_2 = "2018-11-01"

date1 = datetime.strptime(date_1, "%Y-%m-%d")
date2 = datetime.strptime(date_2, "%Y-%m-%d")

delta = date2-date1 
