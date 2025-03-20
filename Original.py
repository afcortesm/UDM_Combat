# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 09:31:30 2025

@author: acortesmoreno
"""

"""
Code to run the original inp within the selected dates
Extract original values for the evaluation parameters
"""

def Original(p,y1,m1,d1,h1,mi1,s1,y2,m2,d2,h2,mi2,s2):
    
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
    
    os.chdir(p)
    
    """
    The following lines read the .inp files in the folder and runs SWMM
    """
    
    inp_files = [f for f in os.listdir(p) if f.endswith('.inp')]
    
    for inp_file in inp_files:
        
        print(f"Running Simulation: {inp_file}")
        
        try:
        
            with pyswmm.Simulation(inp_file) as sim:
                date_1 = datetime.datetime(year=y1,month=m1,day=d1, hour = h1, minute = mi1, second = s1)
                date_2 = datetime.datetime(year=y2,month=m2,day=d2, hour = h2, minute = mi2, second = s2)
                sim.start_time = date_1
                sim.end_time = date_2
                sim.report_start = date_1
                
                start_time = sim.start_time
                end_time = sim.end_time
                total_duration = (end_time-start_time).total_seconds()
                
                for step in sim:
                   
                    current_time = sim.current_time
                    elapsed_time = (current_time - start_time).total_seconds()
                    progress = (elapsed_time / total_duration) * 100
                    sys.stdout.write(f"\rProgress: {progress:.2f}%")
                    sys.stdout.flush()
        
                print(f"\nSimulation {inp_file} completed :)")
            
        except Exception as e: 
            print(f"Error running {inp_file}: {e}")
   
    """
    The following lines read the .rpt and extract the parameters
    """
    
    for inp_file in inp_files:
        
        rpt_file = inp_file.replace('.inp', '.rpt')
        
        inp = swmm_api.read_inp_file(inp_file)
        rpt = swmm_api.read_rpt_file(rpt_file)
    
    Flood = rpt.flow_routing_continuity['Flooding Loss']['Volume_10^6 ltr']
    Evapo = rpt.runoff_quantity_continuity['Evaporation Loss']['Depth_mm']
    WWTP = rpt.outfall_loading_summary.loc['WWTP','Total_Volume_10^6 ltr']
    CSO = rpt.outfall_loading_summary.loc['CSO_overflow','Total_Volume_10^6 ltr']
    Mtss = rpt.outfall_loading_summary.loc['CSO_overflow','Total_TSS_kg']
    
    return(Flood,Evapo,WWTP,CSO,Mtss)     
        
        
        
        