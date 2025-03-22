# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 16:05:51 2025

@author: acortesmoreno
"""

"""
file to test the functions
"""

import os

os.chdir(r"C:\Python\UDM_Battle\Tests")

import pyswmm
import pandas as pd
import numpy as np
import swmm_api
import csv
import sys
import shutil
import pathlib
import Clear
import RunRead
import Original

p0 = r"C:\Users\acortesmoreno\OneDrive - Delft University of Technology\Solutions_UDM\02_Evaluation\05_Original"
p1 = r"C:\Users\acortesmoreno\OneDrive - Delft University of Technology\Solutions_UDM\02_Evaluation\01_Evaluate"
p2 = r"C:\Users\acortesmoreno\OneDrive - Delft University of Technology\Solutions_UDM\02_Evaluation\02_Results"
p3 = r"C:\Users\acortesmoreno\OneDrive - Delft University of Technology\Solutions_UDM\02_Evaluation\03_Storage"
out_decision = 1

# Start date: YYYY/M/D hh:mm:ss
y1 = 2018
m1 = 1
d1 = 1
h1 = 00
mi1 = 00
s1 = 00
# End date: YYYY/M/D hh:mm:ss
y2 = 2019
m2 = 1
d2 = 1
h2 = 00
mi2 = 00
s2 = 00


var = Original.Original(p0,y1,m1,d1,h1,mi1,s1,y2,m2,d2,h2,mi2,s2)

RunRead.RunRead(p1, p2,var[0],var[1],var[3],var[2],var[4],y1,m1,d1,h1,mi1,s1,y2,m2,d2,h2,mi2,s2)

Clear.Clear(p1, p2, p3, out_decision)


