# -*- coding: utf-8 -*-
"""

"""

import os
import pandas as pd
import sqlite3
    
# set working directory
os.chdir(os.path.join('working directory'))

# open database
connection = sqlite3.connect(os.path.join("DPMFA_Plastic_CH.db"))
cursor = connection.cursor()

# extract possible compartment names
cursor.execute("SELECT name,fulllabel FROM compartments")
compartments = cursor.fetchall()

# import table
df = pd.read_csv(os.path.join('./Input Data/DATA_LIFETIMES/Lifetimes_Summary.csv'), sep = ";", decimal = ",")

for comp in df.columns:
    
    if comp == "Year":
        continue
    
    # find short compartment name to use
    for i in range(len(compartments)):
        if compartments[i][1] == comp:
            ind = i
    compname = compartments[ind][0]
    
    # create df to add
    dft = df[['Year',comp]]
    dft = dft.copy()
    dft["Year"] = dft["Year"] - 1
    
    # rename columns
    dft.columns = ['year', 'value']

    # add column with compartment name
    dft['comp'] = compname
    
    # append data to database   
    dft.to_sql('lifetimes', connection, if_exists='append', index = False)
    
# commit changes
connection.commit()

# close connection
connection.close()

print("over")