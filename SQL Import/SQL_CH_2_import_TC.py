

import os
import math
import numpy as np
import pandas as pd
import sqlite3
    
# set working directory
os.chdir(os.path.join('working directory'))

# open database
connection = sqlite3.connect(os.path.join("DPMFA_Plastic_CH.db"))
cursor = connection.cursor()

# extract possible compartment names
cursor.execute("SELECT fulllabel FROM compartments")
compartments = cursor.fetchall()
# flatten the obtained list
compartments = [item for sublist in compartments for item in sublist]

# loop over directories
directory = os.path.join('./Input Data')

for x in os.walk(directory):
    
    # test if "DATA" is in directory name, if not, skip
    if not "DATA" in x[0]:
        continue
    
    # test if "TC" is in directory name, if not, skip
    if not "TC" in x[0]:
        continue
    
    print("\nExploring "+x[0])
    
    # loop over excel files in directories
    for y in x[2]:
                
        # test if "PF_TC_" in file name, if not, skip
        if not "PF_TC" in y:
            continue
        
        # test if "~$" in file name, if yes, skip (temporary invisible excel files)
        if "~$" in y:
            continue
        
        # skip sheets with export flows
        if "inclExport" in y:
            continue
        
        print("--> "+y)
        
        # import excel
        xl = pd.ExcelFile(os.path.join(x[0], y))
        
        # loop over sheets
        for z in xl.sheet_names:
            
            # skip test sheet            
            if z == "test":
                continue
            
            # import excel table
            datatable = pd.read_excel(os.path.join(x[0], y), sheet_name=z, header=None)
            
            # find names of flow and compartments
            floname = datatable.iloc[0,0]
            comp1 = floname.split(" to ")[0]
            comp2 = floname.split(" to ")[1]
            
            # test that compartment names are plausible
            if not comp1 in compartments:
                raise Exception('Compartment "{a}" is not in the database. Details:\nfile = {b}\nsheet = {c}'.format(a = comp1, b = os.path.join(x[0], y), c = z))
                
            if not comp2 in compartments:
                raise Exception('Compartment "{a}" is not in the database. Details:\nfile = {b}\nsheet = {c}'.format(a = comp2, b = os.path.join(x[0], y), c = z))
            
            # remove headers
            data = datatable.drop([0,1,2])
            
            # extract data per material
            anymat = data.iloc[:,np.arange(0,9)+1]
            LDPE   = data.iloc[:,np.arange(0,9)+10]
            HDPE   = data.iloc[:,np.arange(0,9)+19]
            PP     = data.iloc[:,np.arange(0,9)+28]
            PS     = data.iloc[:,np.arange(0,9)+37]
            EPS    = data.iloc[:,np.arange(0,9)+46]
            PVC    = data.iloc[:,np.arange(0,9)+55]
            PET    = data.iloc[:,np.arange(0,9)+64]


          # test that extraction went well, if not, stop execution
            if not all([all(anymat.iloc[:,0] == "any"),
                        all(LDPE.iloc[:,0]   == "LDPE"),
                        all(HDPE.iloc[:,0]   == "HDPE"),
                        all(PP.iloc[:,0]     == "PP"),
                        all(PS.iloc[:,0]     == "PS"),
                        all(EPS.iloc[:,0]    == "EPS"),
                        all(PVC.iloc[:,0]    == "PVC"),
                        all(PET.iloc[:,0]    == "PET")]):
                raise Exception('There is an inconsistency in the material definition in file {a}\n sheet {b}'.format(a = os.path.join(x[0], y), b = z))
            
            # insert into tables
            
            # loop over materials
            for mat in ["LDPE", "HDPE", "PP", "PS", "EPS", "PVC", "PET"]:
                
                if mat == "LDPE":
                    matspec = LDPE
                elif mat == "HDPE":
                    matspec = HDPE
                elif mat == "PP":
                    matspec = PP
                elif mat == "PS":
                    matspec = PS
                elif mat == "EPS":
                    matspec = EPS
                elif mat == "PVC":
                    matspec = PVC
                elif mat == "PET":
                    matspec = PET
                
                # loop over years
                for i in np.arange(0,73):
                    
                    year = i+1950
                    
                    # test if should take data from anymat or mat-specific
                    if not math.isnan(anymat.iloc[i,1]) and math.isnan(matspec.iloc[i,1]):
                        # data of interest
                        doi = anymat.iloc[i,:]

                    elif math.isnan(anymat.iloc[i,1]) and math.isnan(matspec.iloc[i,1]): # if both are nan, raise error
                        raise Exception('There is an inconsistency in the material definition in\nfile = {a}\nsheet = {b}\nmaterial = {c}\nyear = {d}'.format(a = os.path.join(x[0], y), b = z, c = mat, d = year))
                    
                    elif not math.isnan(anymat.iloc[i,1]) and not math.isnan(matspec.iloc[i,1]): # if both are not nan, raise error
                        raise Exception('There is an inconsistency in the material definition in\nfile = {a}\nsheet = {b}\nmaterial = {c}\nyear = {d}'.format(a = os.path.join(x[0], y), b = z, c = mat, d = year))
                        
                    else: # if only the mat-spec is not nan, take that 
                        # data of interest
                        doi = matspec.iloc[i,:]
                        
                    # create string for SQL command
                    format_str = """INSERT INTO transfercoefficients (comp1, comp2, year, mat, value, priority, dqisgeo, dqistemp, dqismat, dqistech, dqisrel, source)
                    VALUES ("{c1}", "{c2}", "{y}", "{mt}", "{val}", "{prio}", "{DQ1}", "{DQ2}", "{DQ3}", "{DQ4}", "{DQ5}", "{src}");"""
                    
                    # reject nan values for DQIS if VALUE is not 0 or 1
                    if doi.hasnans:
                        if not doi.iloc[1] == 0 and not doi.iloc[1] == 1 and not doi.iloc[2] == "rest" and not doi.iloc[2] == "Rest":
                            raise Exception('There is data missing in\nfile = {a}\nsheet = {b}\nmaterial = {c}\nyear = {d}'.format(a = os.path.join(x[0], y), b = z, c = mat, d = year))
                    
                    # define priority
                    if doi.iloc[2] == "rest" or doi.iloc[2] == "Rest":
                        p = 1
                    else:
                        p = 2
                    
                    sql_command = format_str.format(c1 = comp1,
                                                    c2 = comp2,
                                                    y = year,
                                                    mt = mat,
                                                    val = doi.iloc[1],
                                                    prio = p,
                                                    DQ1 = doi.iloc[3],
                                                    DQ2 = doi.iloc[4],
                                                    DQ3 = doi.iloc[5], 
                                                    DQ4 = doi.iloc[6],
                                                    DQ5 = doi.iloc[7],
                                                    src = doi.iloc[2])
                    
                    cursor.execute(sql_command)

# commit changes
connection.commit()

# close connection
connection.close()

print("over")
