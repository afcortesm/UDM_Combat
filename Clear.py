# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 10:39:15 2025

@author: acortesmoreno
"""

"""
Code to keep the folders organised
After running swmm, the RunRead code copies and pastes the inp and rpt into the results folder
We should store the inp and rpt and free space in the key folders

f1 -> folder with the inp to be modelled
f2 -> folder with the result files
f3 -> folder to store the results
out_decision: 1 or 0. 1 to delete the .out files, 0 to keep and store the .out files

"""

def Clear(f1,f2,f3,out_decision):
    
    
    import os
    import pyswmm
    import pandas as pd
    import numpy as np
    import swmm_api
    import csv
    import sys
    import shutil
    import pathlib
    
       
    folder_1 = f1
    folder_2 = f2
    folder_3 = f3
    
    """
    The following lines copy the inp and the rpt to the results folder in order to free space
    """
            
    for file_name in os.listdir(folder_1):
        if file_name.endswith((".inp",".rpt")):
            source_path = os.path.join(folder_1,file_name)
            destination_path = os.path.join(folder_3,file_name)
            shutil.copy2(source_path,destination_path)
            os.remove(source_path)
            
    print("All .inp and .rpt files have been copied! ;)")
    
    for file_name in os.listdir(folder_2):
        if file_name.endswith((".inp",".rpt")):
            source_path = os.path.join(folder_2,file_name)
            os.remove(source_path)
            
    print("All files have been deleted")
    
    if out_decision == 1:
        for file_name in os.listdir(folder_1):
            if file_name.endswith((".out")):
                source_path = os.path.join(folder_1,file_name)
                os.remove(source_path)
        print("The .out files have been deleted")
    elif out_decision ==0:
        if file_name.endswith((".out")):
            source_path = os.path.join(folder_1,file_name)
            destination_path = os.path.join(folder_3,file_name)
            shutil.copy2(source_path,destination_path)
        print("The out files have been stored")
    else:
        print("Nothing was done")
                


        