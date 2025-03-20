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

p0 = r"C:\Python\UDM_Battle\Original"
p1 = r"C:\Python\UDM_Battle\To_Evaluate"
p2 = r"C:\Python\UDM_Battle\Results"
p3 = r"C:\Python\UDM_Battle\Storage"
out_decision = 1
y1 = 2018
m1 = 8
d1 = 24
h1 = 20
mi1 = 45
s1 = 00
y2 = 2018
m2 = 8
d2 = 24
h2 = 23
mi2 = 59
s2 = 00


var = Original.Original(p0,y1,m1,d1,h1,mi1,s1,y2,m2,d2,h2,mi2,s2)

RunRead.RunRead(p1, p2,var[0],var[1],var[3],var[2],var[4],y1,m1,d1,h1,mi1,s1,y2,m2,d2,h2,mi2,s2)

Clear.Clear(p1, p2, p3, out_decision)


