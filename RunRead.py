# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 11:48:24 2025

@author: acortesmoreno
"""

"""
Code to run every .inp file and extract the values for the evaluation parameters
"""

"""
Code to read .inp, run the simulation and read the .rpt
"""
p1 = r"C:\Python\UDM_Battle\To_Evaluate"
p2 = r"C:\Python\UDM_Battle\Results"

"""
p1 is the path to the folder where the .inp to run are stored
p2 is the path to the folder where the .inp and .rpt are saved and the results are extracted
"""

def RunRead(p1,p2,fl,ev,cs,ww,mt,y1,m1,d1,h1,mi1,s1,y2,m2,d2,h2,mi2,s2): 

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
    
    # Define the path to the folder in which the inp and rpt files are stored
    
    path = p1
    
    path_2 = p2
    
    os.chdir(path)
    
    """
    The following lines read the .inp files in the folder and runs SWMM
    """
    
    inp_files = [f for f in os.listdir(path) if f.endswith('.inp')]
    
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
    The following lines copy the inp and the rpt to the results folder in order to free space
    """
            
    for file_name in os.listdir(path):
        if file_name.endswith((".inp",".rpt")):
            source_path = os.path.join(path,file_name)
            destination_path = os.path.join(path_2,file_name)
            
            shutil.copy2(source_path,destination_path)
            
    print("All .inp and .rpt files have been copied! ;)")
    
    """
    Lines to evaluate the inp and rpt
    """
    
    os.chdir(path_2)
    
    if "results.csv" in os.listdir(path_2):
        results = pd.read_csv("Results.csv")
    else:
        results = pd.DataFrame(columns=['Name','Total_Cost','Biodiversity','Flood','Evaporation','Flow_WWTP','CSO','Pollutant_Load'])
        
    
    
    inp_files = [f for f in os.listdir(path) if f.endswith('.inp')]
    
    for inp_file in inp_files:
        
        rpt_file = inp_file.replace('.inp', '.rpt')
        
        inp = swmm_api.read_inp_file(inp_file)
        rpt = swmm_api.read_rpt_file(rpt_file)
        
        LIDs = inp['LID_USAGE']
        
        if not LIDs:
            Tot_Cost = 0
            Biodiversity = 0
        else:
        
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
            
            BGIs['cost'] = BGIs['area']*BGIs['lid'].map(lid_unit_costs) + BGIs['lid'].map(lid_base_costs)
                
            Tot_Cost = BGIs['cost'].sum()
             
            
            Bio_sum = BGIs.groupby('lid')['area'].sum()
            
            Bio_results = {lid: Bio_sum.get(lid, 0) for lid in lid_types}
            
            Biodiversity = min(int(Bio_results["Intensive_green_roof"]), int(Bio_results["Bio_retention_system"]), int(Bio_results["Dry_swale"]), int(Bio_results["Extensive_green_roof"]))
        
        
        Flood = rpt.flow_routing_continuity['Flooding Loss']['Volume_10^6 ltr']
        Evapo = rpt.runoff_quantity_continuity['Evaporation Loss']['Depth_mm']
        WWTP = rpt.outfall_loading_summary.loc['WWTP','Total_Volume_10^6 ltr']
        CSO = rpt.outfall_loading_summary.loc['CSO_overflow','Total_Volume_10^6 ltr']
        Mtss = rpt.outfall_loading_summary.loc['CSO_overflow','Total_TSS_kg']
        
        """
        The following lines have the values for the parameters in the original .inp
        These values depend on the time period analysed
        """
        
        or_flood = fl
        or_evapo = ev
        or_wwtp = ww
        or_cso = cs
        or_mtss = mt
        
        new_row = pd.DataFrame([{'Name': (pathlib.Path(inp_file).stem),'Total_Cost':Tot_Cost,'Biodiversity':Biodiversity,'Flood': or_flood - Flood,'Evaporation':Evapo - or_evapo,'Flow_WWTP':WWTP - or_wwtp,'CSO':or_cso - CSO,'Pollutant_Load':or_mtss - Mtss}])
        nametostore =  pathlib.Path(inp_file).stem
        result_name = f"{nametostore}.csv"
        new_row.to_csv(result_name, index=False)
        results = pd.concat([results,new_row], ignore_index=True)
    
    results.to_csv("Results.csv", index=False)
