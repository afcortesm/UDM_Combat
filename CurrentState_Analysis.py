# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 11:09:35 2025

@author: acortesmoreno
"""

"""
This code is proposed for the analysis of the current state of the network
    as part of the UDM Combat of retroffitting of BGIs

The objective of the code is to extract the initial conditions for the 
    evaluation parameters from the current state while also performing a 
    sensitivity analysis of the temporal evolution of the parameters
"""

"""
1st part - Extraction of the initial conditions
"""


import os
import pyswmm
import pandas as pd
import numpy as np
import swmm_api
import csv
import tkinter as tk
from tkinter import filedialog

# Create a hidden root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Open file dialog

path = filedialog.askopenfilename(title="Enter the path")

if os.path.exists(path):
    print("File exists!")
else:
    print("File not found.")
    
os.chdir(path)


