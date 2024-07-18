import numpy as np
import glob
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from math import log10, floor
import pandas as pd


pc = ["Consumer Films",
      "Consumer Bags",
      "Consumer Bottles",
      "Other Consumer Packaging",
      "Other Non Consumer Films",
      "Non Consumer Bags",
      "Other Non Consumer Packaging",

      "Agricultural Packaging Films",
      "Agricultural Packaging Bottles",
      "Agricultural Films",
      "Agricultural Pipes",
      "Other Agricultural Plastics",
      "Agrotextiles",

      "Building Packaging Films",
      "Pipes and Ducts",
      "Insulation",
      "Wall and Floor Coverings",
      "Windows, Profiles and Fitted Furniture",
      "Lining",
      "Geotextiles",
      "Building Textiles",

      "Automotive",
      "Mobility Textiles",

      "Electrical and Electronic Equipment",

      "Household Plastics",
      "Furniture",
      "Fabric Coatings",
      "Personal Care and Cosmetic Products",
      "Other Plastic Products",

      "Clothing",
      "Technical Clothing",
      "Household Textiles",
      "Technical Household Textiles",

      "Hygiene and Medical Textiles",
      "Other Technical Textiles"]

# import and print all the stock data
Stocks = {}
for mat in ["LDPE", "HDPE", "PP", "PS", "EPS", "PVC", "PET"]:
    Stocks[mat] = []
    listfiles = glob.glob(r'.\csv\stocks_' + mat + '*.csv')

    for comp in pc:
        file = r'.\csv\stocks_' + mat + '_' + comp + '.csv'

        if file in listfiles:
            temp = np.genfromtxt(file, delimiter=' ')
            mean_val = np.mean(temp[:, -1])
            sd_val = np.std(temp[:, -1])
            Stocks[mat].append((mean_val, sd_val))
            print(f"{mat}+{comp}: {mean_val} + {sd_val}")
        else:
            Stocks[mat].append((0, 0))
            print(f"{mat}+{comp}: {0} + {0}")


input = ["Packaging (sector)",
         "Building and Construction (sector)",
         "Agriculture (sector)",
         "Automotive (sector)",
         "Electrical and Electronic Equipment (sector)",
         "Other Plastic Products (sector)",
         "Pre-consumer Waste Collection",
         "Clothing (sector)",
         "Household Textiles (sector)",
         "Technical Textiles (sector)",
         "Transport",]

# import and print all the inflow data
Inflows = {}
for mat in ["LDPE", "HDPE", "PP", "PS", "EPS", "PVC", "PET"]:
    Inflows[mat] = []
    listfiles = glob.glob(r'.\csv\loggedInflows_' + mat + '*.csv')

    for comp in input:
        file = r'.\csv\loggedInflows_' + mat + '_' + comp + '.csv'

        if file in listfiles:
            temp = np.genfromtxt(file, delimiter=' ')
            mean_val = np.mean(temp[:, -1])
            sd_val = np.std(temp[:, -1])
            Inflows[mat].append((mean_val, sd_val))
            print(f"{mat} + {comp}: {mean_val} + {sd_val}")
        else:
            Inflows[mat].append((0, 0))
            print(f"{mat} + {comp}: {0} + {0}")