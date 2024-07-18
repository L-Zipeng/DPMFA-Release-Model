# -*- coding: utf-8 -*-


import os

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

# path to data to import
path = os.path.join('./Input Data', 'PF_Inflows_Summary.xlsx')

# import excel
xl = pd.ExcelFile(path)

# loop over sheets
for z in xl.sheet_names:

    # skip test sheet            
    if z == "Geyer_GlobalPlastics":
        continue

    print("Importing " + z)

    # import excel table
    datatable = pd.read_excel(path, sheet_name=z, header=None)

    # find names of compartment
    comp = z

    if comp == "EEE":
        comp = "Electrical and Electronic Equipment (sector)"
    elif comp == "BnC":
        comp = "Building and Construction (sector)"

    # test that compartment names are plausible
    if not comp in compartments:
        raise Exception('Compartment "{a}" is not in the database.'.format(a=comp))

    # remove headers
    data = datatable.drop([0, 1])

    # importing data for inputs with single data point                                                                                      
    if not z == "Packaging (sector)":
        # extract data per material
        LDPE = data.iloc[np.arange(0, 73), np.arange(0, 9) + 1]
        HDPE = data.iloc[np.arange(0, 73), np.arange(0, 9) + 10]
        PP = data.iloc[np.arange(0, 73), np.arange(0, 9) + 19]
        PS = data.iloc[np.arange(0, 73), np.arange(0, 9) + 28]
        EPS = data.iloc[np.arange(0, 73), np.arange(0, 9) + 37]
        PVC = data.iloc[np.arange(0, 73), np.arange(0, 9) + 46]
        PET = data.iloc[np.arange(0, 73), np.arange(0, 9) + 55]

        # test that extraction went well, if not, stop execution
        if not all([all(LDPE.iloc[:, 0] == "LDPE"),
                    all(HDPE.iloc[:, 0] == "HDPE"),
                    all(PP.iloc[:, 0] == "PP"),
                    all(PS.iloc[:, 0] == "PS"),
                    all(EPS.iloc[:, 0] == "EPS"),
                    all(PVC.iloc[:, 0] == "PVC"),
                    all(PET.iloc[:, 0] == "PET")]):
            raise Exception('There is an inconsistency in the material definition in sheet {b}'.format(b=z))

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
            for i in np.arange(0, 73):
                year = i + 1950

                # data of interest
                doi = matspec.iloc[i, :]

                # create string for SQL command
                format_str = """INSERT INTO input (comp, year, mat, value, dqisgeo, dqistemp, dqismat, dqistech, dqisrel, source)
                VALUES ("{c}", "{y}", "{mt}", "{val}", "{DQ1}", "{DQ2}", "{DQ3}", "{DQ4}", "{DQ5}", "{src}");"""

                sql_command = format_str.format(c=comp,
                                                y=year,
                                                mt=mat,
                                                val=doi.iloc[1],
                                                DQ1=doi.iloc[3],
                                                DQ2=doi.iloc[4],
                                                DQ3=doi.iloc[5],
                                                DQ4=doi.iloc[6],
                                                DQ5=doi.iloc[7],
                                                src=doi.iloc[2])

                cursor.execute(sql_command)

    # else for packaging (two data points per year and mat)
    else:

        # extract data per material
        LDPE1 = data.iloc[np.arange(0, 73), np.arange(0, 9) + 1]
        LDPE2 = data.iloc[np.arange(0, 73), np.arange(0, 9) + 10]
        HDPE1 = data.iloc[np.arange(0, 73), np.arange(0, 9) + 19]
        HDPE2 = data.iloc[np.arange(0, 73), np.arange(0, 9) + 28]
        PP1 = data.iloc[np.arange(0, 73), np.arange(0, 9) + 37]
        PP2 = data.iloc[np.arange(0, 73), np.arange(0, 9) + 46]
        PS1 = data.iloc[np.arange(0, 73), np.arange(0, 9) + 55]
        PS2 = data.iloc[np.arange(0, 73), np.arange(0, 9) + 64]
        EPS1 = data.iloc[np.arange(0, 73), np.arange(0, 9) + 73]
        EPS2 = data.iloc[np.arange(0, 73), np.arange(0, 9) + 82]
        PVC1 = data.iloc[np.arange(0, 73), np.arange(0, 9) + 91]
        PVC2 = data.iloc[np.arange(0, 73), np.arange(0, 9) + 100]
        PET1 = data.iloc[np.arange(0, 73), np.arange(0, 9) + 109]
        PET2 = data.iloc[np.arange(0, 73), np.arange(0, 9) + 118]

        # test that extraction went well, if not, stop execution
        if not all([all(LDPE1.iloc[:, 0] == "LDPE"),
                    all(LDPE2.iloc[:, 0] == "LDPE"),
                    all(HDPE1.iloc[:, 0] == "HDPE"),
                    all(HDPE2.iloc[:, 0] == "HDPE"),
                    all(PP1.iloc[:, 0] == "PP"),
                    all(PP2.iloc[:, 0] == "PP"),
                    all(PS1.iloc[:, 0] == "PS"),
                    all(PS2.iloc[:, 0] == "PS"),
                    all(EPS1.iloc[:, 0] == "EPS"),
                    all(EPS2.iloc[:, 0] == "EPS"),
                    all(PVC1.iloc[:, 0] == "PVC"),
                    all(PVC2.iloc[:, 0] == "PVC"),
                    all(PET1.iloc[:, 0] == "PET"),
                    all(PET2.iloc[:, 0] == "PET")]):
            raise Exception('There is an inconsistency in the material definition in sheet {b}'.format(b=z))

        # insert into tables

        # loop over materials 
        for mat in ["LDPE", "HDPE", "PP", "PS", "EPS", "PVC", "PET"]:

            if mat == "LDPE":
                matspec1 = LDPE1
                matspec2 = LDPE2
            elif mat == "HDPE":
                matspec1 = HDPE1
                matspec2 = HDPE2
            elif mat == "PP":
                matspec1 = PP1
                matspec2 = PP2
            elif mat == "PS":
                matspec1 = PS1
                matspec2 = PS2
            elif mat == "EPS":
                matspec1 = EPS1
                matspec2 = EPS2
            elif mat == "PVC":
                matspec1 = PVC1
                matspec2 = PVC2
            elif mat == "PET":
                matspec1 = PET1
                matspec2 = PET2

            # loop over years
            for i in np.arange(0, 73):
                year = i + 1950

                # data of interest
                doi = matspec1.iloc[i, :]

                # create string for SQL command
                format_str = """INSERT INTO input (comp, year, mat, value, dqisgeo, dqistemp, dqismat, dqistech, dqisrel, source)
                VALUES ("{c}", "{y}", "{mt}", "{val}", "{DQ1}", "{DQ2}", "{DQ3}", "{DQ4}", "{DQ5}", "{src}");"""

                sql_command = format_str.format(c=comp,
                                                y=year,
                                                mt=mat,
                                                val=doi.iloc[1],
                                                DQ1=doi.iloc[3],
                                                DQ2=doi.iloc[4],
                                                DQ3=doi.iloc[5],
                                                DQ4=doi.iloc[6],
                                                DQ5=doi.iloc[7],
                                                src=doi.iloc[2])

                cursor.execute(sql_command)

                # data of interest
                doi = matspec2.iloc[i, :]

                # create string for SQL command
                format_str = """INSERT INTO input (comp, year, mat, value, dqisgeo, dqistemp, dqismat, dqistech, dqisrel, source)
                VALUES ("{c}", "{y}", "{mt}", "{val}", "{DQ1}", "{DQ2}", "{DQ3}", "{DQ4}", "{DQ5}", "{src}");"""

                sql_command = format_str.format(c=comp,
                                                y=year,
                                                mt=mat,
                                                val=doi.iloc[1],
                                                DQ1=doi.iloc[3],
                                                DQ2=doi.iloc[4],
                                                DQ3=doi.iloc[5],
                                                DQ4=doi.iloc[6],
                                                DQ5=doi.iloc[7],
                                                src=doi.iloc[2])

                cursor.execute(sql_command)

# commit changes
connection.commit()

# close connection
connection.close()

print("over")