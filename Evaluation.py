# -*- coding: utf-8 -*-
"""
Created on Fri Mar  21 10:27:00 2025

@author: acortesmoreno
"""

"""
This code runs a group of .inp and read the evaluation parameters for the UDM NBS Combat. 
The code requires:
 - Start and end date for the .inp
 - Three folders:
    1) Folder with the .inp to be tested
    2) Folder for storing the results
    
"""

def Evaluate(folder_inp, folder_results, initial_flood, initial_evapo, 
             initial_cso, initial_wastewater, initial_pollutant, year_1, 
             month_1, day_1, hour_1, minute_1, second_1, year_2, month_2,
             day_2, hour_2, minute_2, second_2): 
    
    # The following lines import usefull libraries (safeguard point)
    import os
    import pyswmm
    import pandas as pd
    import numpy as np
    import swmm_api
    import csv
    import sys
    import shutil
    import pathlib
    import datetime

    # Set the working path in the .inp folder

    os.chdir(folder_inp)

    # Read the .inp and run the different simulations using the selected dates

    inp_files = [f for f in os.listdir(folder_inp) if f.endswith('.inp')]

    for inp_file in inp_files: 

        print(f"Running solution: {inp_file}")

        try: 
            
            with pyswmm.Simulation(inp_file) as sim:
                date_1 = datetime.datetime(year=year_1, month=month_1, day=day_1,
                                           hour=hour_1,minute=minute_1, second=second_1)
                date_2 = datetime.datetime(year=year_2, month=month_2, day=day_2,
                                           hour=hour_2,minute=minute_2, second=second_2)
                sim.start_time = date_1
                sim.report_start = date_1
                sim.end_time = date_2

                # Create variables to track the progress of the simulation

                start_time = sim.start_time
                end_time = sim.end_time
                total_duration = (end_time - start_time).total_seconds()

                for step in sim: 

                    current_time = sim.current_time
                    elapsed_time = (current_time - start_time).total_seconds()
                    progress = (elapsed_time / total_duration) * 100
                    sys.stdout.write(f"\rProgress: {progress:.2f}%")
                    sys.stdout.flush()

                # Message marking the end of the simulation of the file
                print(f"\nSimulation {inp_file} completed! ;)")
        except Exception as e: 
            print(f"Error running {inp_file}: {e}")
    
    # Once all the .inp are used in SWMM, the .inp and .rpt are moved to the 
    # results folder

    for file_name in os.listdir(folder_inp):
        if file_name.endswith((".inp",".rpt")):
            source_path = os.path.join(folder_inp,file_name)
            destination_path = os.path.join(folder_results,file_name)
            shutil.copy2(source_path,destination_path)
    
    print("The .inp and .rpt are now in the results file! :)")

    os.chdir(folder_results)

    # Check if there is a results file available to append the new results

    if "Results.csv" in os.listdir(folder_results):
        results = pd.read_csv("Results.csv")
    else:
        Results = pd.DataFrame(columns=['Name','Total_Cost','Biodiversity','Flood',
                                        'Evaporation','Flow_WWTP','CSO',
                                        'Pollutant_Load'])
    
    
                