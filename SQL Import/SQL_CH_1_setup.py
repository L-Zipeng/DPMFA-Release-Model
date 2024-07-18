# -*- coding: utf-8 -*-
"""

To run this script, SQLite needs to be installed on the computer.
"""

import os
import sqlite3
import numpy as np
import pandas as pd

# set working directory to your working directory
os.chdir(os.path.join('working directory'))

# create or open database
connection = sqlite3.connect("DPMFA_Plastic_CH.db")
cursor = connection.cursor()


# create a table for compartments
cursor.execute("""
               CREATE TABLE IF NOT EXISTS compartments (
               name TEXT,
               fulllabel TEXT,
               type TEXT,
               PRIMARY KEY(fulllabel)
               );""")

# import compartment table
data = pd.read_excel(os.path.join("./Compartments.xlsx"), sheet_name="Rank")

# insert into database
for i in np.arange(0,data.shape[0]):
    
    format_str = """INSERT OR IGNORE INTO compartments (name, fulllabel, type)
    VALUES ("{a1}", "{a2}", "{a3}");"""

    sql_command = format_str.format(a1 = data.loc[i,:][0],
                                    a2 = data.loc[i,:][1],
                                    a3 = data.loc[i,:][2])
    cursor.execute(sql_command)


# create a table for materials
cursor.execute("""
               CREATE TABLE IF NOT EXISTS materials (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT
               );""")

# insert into database
for i in ["LDPE", "HDPE", "PP", "PS", "EPS", "PVC", "PET"]:
    
    format_str = """INSERT INTO materials (name)
    VALUES ("{a1}");"""
    
    sql_command = format_str.format(a1=i)
    cursor.execute(sql_command)


# create a table for transfer coefficients
cursor.execute("""
               CREATE TABLE IF NOT EXISTS transfercoefficients (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               comp1 INTEGER NOT NULL,
               comp2 INTEGER NOT NULL,
               year INTEGER,
               mat INTEGER NOT NULL,
               value DOUBLE,
               priority INTEGER NOT NULL,
               dqisgeo INTEGER NOT NULL,
               dqistemp INTEGER NOT NULL,
               dqismat INTEGER NOT NULL,
               dqistech INTEGER NOT NULL,
               dqisrel INTEGER NOT NULL,
               source TEXT,
               FOREIGN KEY(comp1) REFERENCES compartments(fulllabel),
               FOREIGN KEY(comp2) REFERENCES compartments(fulllabel),
               FOREIGN KEY(mat) REFERENCES materials(name)
               );""")


# create a table for input
cursor.execute("""
               CREATE TABLE IF NOT EXISTS input (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               comp TEXT,
               year INTEGER,
               mat TEXT,
               value DOUBLE,
               dqisgeo INTEGER NOT NULL,
               dqistemp INTEGER NOT NULL,
               dqismat INTEGER NOT NULL,
               dqistech INTEGER NOT NULL,
               dqisrel INTEGER NOT NULL,
               source TEXT,
               FOREIGN KEY(comp) REFERENCES compartments(fulllabel),
               FOREIGN KEY(mat) REFERENCES materials(id)
               );""")


# create a table for lifetimes
cursor.execute("""
               CREATE TABLE IF NOT EXISTS lifetimes (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               comp TEXT,
               year INTEGER,
               value DOUBLE,
               FOREIGN KEY(comp) REFERENCES compartments(fulllabel)
               );""")


# commit changes
connection.commit()

# close connection
connection.close()

print("over")