# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 10:32:58 2025

@author: acortesmoreno
"""

"""
Code to evaluate the time series of the evaluation parameters of the system in the inital state
"""

# Usefull libraries throuout the  evaluation process

import os
import pyswmm
import pandas as pd
import numpy as np
import swmm_api
import csv
import matplotlib.pyplot as plt

# Define the path to the folder in which the inp and rpt files are stored

path = r"C:\Python\UDM_Battle\Initial_Conditions"

os.chdir(path)

"""
First we read the precipitation and the temperature files and create pandas to store them 
"""

rain_data = pd.read_csv("rain2018.dat", delimiter=r"\s+", header=None, names=['Station','Year','Month',"Day",'Hour','Minute',"Value"])
temp_data = pd.read_csv("temp2018.dat", delimiter=r"\s+", header=None, names=['Station','Year','Month',"Day",'Hour','Minute',"Value"])

rain_data['Date'] = pd.to_datetime(rain_data[["Year","Month","Day","Hour","Minute"]],format='%YYYY%mm%d %H:%M')
temp_data['Date'] = pd.to_datetime(temp_data[["Year","Month","Day","Hour","Minute"]],format='%YYYY%mm%d %H:%M')

rain_data = rain_data[["Date","Value"]]
temp_data = temp_data[["Date","Value"]]

rain_data.set_index('Date',inplace=True)
temp_data.set_index('Date',inplace=True)


rain_data.plot(color='blue')
plt.ylabel("Precipitation [mm]")
plt.title("Precipitation")

temp_data.plot(linewidth=0.5, color='red')
plt.ylabel("Temperature [C]")
plt.title("Temperature")

"""
The next step is to analyse the change of the parameters in time
The parameters regarding the LIDs are fixed (cost and biodiversity)
The other parameters can be obtained from the .out file
"""

file = [f for f in os.listdir(path) if f.endswith('.out')]

out_file = swmm_api.read_out_file(file[0])

"""
From the output file we need to look for the relevant time series and store them in pandas
The units in the out and rpt file are different, so this need to be considered
"""

Flood_series = out_file.get_part('system','', 'flooding')*60/(1e6)
WWTP_series= out_file.get_part('node','WWTP','total_inflow')*60/(1e6)
CSO_series = out_file.get_part('node','CSO_overflow','total_inflow')*60/(1e6)
Evapo_series = out_file.get_part('system','','evaporation')/(24*60)
Pollutant_series = out_file.get_part('node','CSO_overflow','TSS')*CSO_series

# The fixed values are the initial parameters obtained from the original rpt

Flood_cummulative = Flood_series.cumsum()
Flood_influence = Flood_cummulative/0.296


WWTP_cummulative = WWTP_series.cumsum()
WWTP_influence = WWTP_cummulative/436.029


CSO_cummulative = CSO_series.cumsum()
CSO_influence = CSO_cummulative/65.424


Evapo_cummulative = Evapo_series.cumsum()
Evapo_influence = Evapo_cummulative/93.322

Pollutant_cummulative = Pollutant_series.cumsum()
Pollutant_influence = Pollutant_cummulative/5302.518


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




