# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 10:32:58 2025

@author: acortesmoreno - lauragonzalez
"""

"""
Code to evaluate run TOPSIS and evaluate all the available solutions
"""

def TOPSIS(path):

    import pandas as pd
    import numpy as np
    import os

    os.chdir(r"C:\Python\UDM_Battle\Results")

    """
    The following line reads the files and looks for the Result file
    """

    results = pd.read_csv("Results.csv")

    # If the biodiversity is always 0, TOPSIS fails. So we need to 
    # check this condition

    
    if results["Biodiversity"].var() == 0:
        results = results.drop(columns=["Biodiversity"])
        criteria_types = np.array([-1,1,1,1,1,1])
    else:
        criteria_types = np.array([-1,1,1,1,1,1,1])
    


    # Extract the names 

    alternatives =  results["Name"].values
    criteria_matrix = results.iloc[:,1:].values

    normalized_matrix =  criteria_matrix / np.sqrt((criteria_matrix**2).sum(axis=0))

    weights = np.ones(len(criteria_types)) / len(criteria_types)

    weighted_matrix = normalized_matrix * weights

    ideal_positive = np.max(weighted_matrix * (criteria_types == 1), axis=0) + \
                 np.min(weighted_matrix * (criteria_types == -1), axis=0)

    ideal_negative = np.min(weighted_matrix * (criteria_types == 1), axis=0) + \
                 np.max(weighted_matrix * (criteria_types == -1), axis=0)

    dist_positive = np.sqrt(((weighted_matrix - ideal_positive) ** 2).sum(axis=1))
    dist_negative = np.sqrt(((weighted_matrix - ideal_negative) ** 2).sum(axis=1))

    relative_closeness = dist_negative / (dist_positive + dist_negative)

    topsis = pd.DataFrame({
        "Name": alternatives,
        "Topsis_score": relative_closeness
    }).sort_values(by="Topsis_score", ascending = False)

    topsis.to_csv(Topsis.csv,index=False)

