

import os
import pandas as pd
import numpy as np
import glob
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

nperiods = 73
startYear = 2000
endYear = 2022


### Cons inflow ###############################################################

Cons = {}
for mat in ["LDPE","HDPE","PP","PS","EPS","PVC","PET"]:

    # list all files with inflows for mat
    listfiles = glob.glob(r'.\csv/loggedInflows_'+mat+'*.csv')

    Cons[mat] = np.zeros((10000,73))
    for cat in pc:
        file = r'.\csv\loggedInflows_'+mat+'_'+cat+'.csv'

        if file in listfiles:
            tempdata = genfromtxt(file, delimiter=' ')*1000
            Cons[mat] = Cons[mat]+tempdata

### Cons stock ################################################################

Stock = {}
for mat in ["LDPE","HDPE","PP","PS","EPS","PVC","PET"]:

    # list all files with inflows for mat
    listfiles = glob.glob(r'.\csv\stocks_'+mat+'*.csv')

    Stock[mat] = np.zeros((10000,73))
    for cat in pc:
        file = r'.\csv\stocks_'+mat+'_'+cat+'.csv'

        if file in listfiles:
            tempdata = genfromtxt(file, delimiter=' ')*1000
            Stock[mat] = Stock[mat]+tempdata

### Standard sinks ############################################################

Elim = {}
Lf = {}
Nsoilma = {}
Nsoilmi = {}
SWatma = {}
SWatmi = {}
Rs = {}
Sub = {}
Asoilma = {}
Asoilmi = {}
Rsoilma = {}
Rsoilmi = {}

for mat in ["LDPE","HDPE","PP","PS","EPS","PVC","PET"]:

    # list all files with inflows for mat
    listfiles = glob.glob(r'.\csv\sinks_'+mat+'*.csv')

    file = r'.\csv\sinks_'+mat+'_Incineration.csv'
    if file in listfiles:
        Elim[mat] = genfromtxt(file, delimiter=' ')*1000
    else:
        Elim[mat] = np.zeros((10000,73))

    file = r'.\csv\sinks_'+mat+'_Landfill.csv'
    if file in listfiles:
        Lf[mat] = genfromtxt(file, delimiter=' ')*1000
    else:
        Lf[mat] = np.zeros((10000,73))

    file = r'.\csv\sinks_'+mat+'_Road Side (macro).csv'
    if file in listfiles:
        Rs[mat] = genfromtxt(file, delimiter=' ')*1000
    else:
        Rs[mat] = np.zeros((10000,73))

    file = r'.\csv\sinks_' + mat + '_Sub-surface (micro).csv'
    if file in listfiles:
        Sub[mat] = genfromtxt(file, delimiter=' ') * 1000
    else:
        Sub[mat] = np.zeros((10000, 73))

    file = r'.\csv\sinks_' + mat + '_Agricultural Soil (macro).csv'
    if file in listfiles:
        Asoilma[mat] = genfromtxt(file, delimiter=' ') * 1000
    else:
        Asoilma[mat] = np.zeros((10000, 73))

    file = r'.\csv\sinks_' + mat + '_Agricultural Soil (micro).csv'
    if file in listfiles:
        Asoilmi[mat] = genfromtxt(file, delimiter=' ') * 1000
    else:
        Asoilmi[mat] = np.zeros((10000, 73))

    file = r'.\csv\sinks_' + mat + '_Natural Soil (macro).csv'
    if file in listfiles:
        Nsoilma[mat] = genfromtxt(file, delimiter=' ') * 1000
    else:
        Nsoilma[mat] = np.zeros((10000, 73))

    file = r'.\csv\sinks_' + mat + '_Natural Soil (micro).csv'
    if file in listfiles:
        Nsoilmi[mat] = genfromtxt(file, delimiter=' ') * 1000
    else:
        Nsoilmi[mat] = np.zeros((10000, 73))

    file = r'.\csv\sinks_' + mat + '_Residential Soil (macro).csv'
    if file in listfiles:
        Rsoilma[mat] = genfromtxt(file, delimiter=' ') * 1000
    else:
        Rsoilma[mat] = np.zeros((10000, 73))

    file = r'.\csv\sinks_' + mat + '_Residential Soil (micro).csv'
    if file in listfiles:
        Rsoilmi[mat] = genfromtxt(file, delimiter=' ') * 1000
    else:
        Rsoilmi[mat] = np.zeros((10000, 73))

    file = r'.\csv\sinks_' + mat + '_Surface Water (macro).csv'
    if file in listfiles:
        SWatma[mat] = genfromtxt(file, delimiter=' ') * 1000
    else:
        SWatma[mat] = np.zeros((10000, 73))

    file = r'.\csv\sinks_' + mat + '_Surface Water (micro).csv'
    if file in listfiles:
        SWatmi[mat] = genfromtxt(file, delimiter=' ') * 1000
    else:
        SWatmi[mat] = np.zeros((10000, 73))

### Recycling ############################################################

Rec = {}

for mat in ["LDPE","HDPE","PP","PS","EPS","PVC","PET"]:

    # list all files with inflows for mat
    listfiles = glob.glob(r'.\csv\sinks_'+mat+'*.csv')

    # origin compartments included in "export of recyclable material"
    orig = ["Automotive Parts Reuse",
            "Material Reuse",
            "Textile Reuse"]
    toadd = np.zeros((10000,73))

    for comp in orig:
        file = r'.\csv\sinks_'+mat+'_'+comp+'.csv'
        if file in listfiles:
            temp = genfromtxt(file, delimiter=' ')*1000
            toadd = toadd + temp

    Rec[mat] = toadd


### Export ####################################################################

# find possible flows to export (need to check this if change the system)
#    glob.glob('.\csv\loggedOutflows_*_to_Export.csv')

RecExp = {}
Export = {}

for mat in ["LDPE","HDPE","PP","PS","EPS","PVC","PET"]:
    # list files for loop
    listfiles = glob.glob(r'.\csv\loggedOutflows_'+mat+'*_to_Export.csv')

    # origin compartments included in "export of recyclable material"
    orig = ["Packaging Collection",
            "Packaging Recycling",
            "Textile Waste Collection"]
    toadd = np.zeros((10000,73))

    for comp in orig:
        file = r'.\csv\loggedOutflows_'+mat+'_'+comp+'_to_Export.csv'
        if file in listfiles:
            temp = genfromtxt(file, delimiter=' ')*1000
            toadd = toadd + temp

    # sum over periods (since calculating this from flows and not a sink)
    RecExp[mat] = toadd.sum(axis=1)

    # origin compartments included in "other exports"
    orig = ["Transport",
            "Automotive (sector)",
            "Automotive",
            "Electrical and Electronic Equipment",
            "Fibre Production",
            "Mobility Textiles",
            "Non-Textile Manufacturing"]

    toadd = np.zeros((10000,73))
    for comp in orig:
        file = r'.\csv\loggedOutflows_'+mat+'_'+comp+'_to_Export.csv'
        if file in listfiles:
            temp = genfromtxt(file, delimiter=' ')*1000
            toadd = toadd + temp
    # sum over periods    
    Export[mat] = toadd.sum(axis=1)

### Print out #################################################################

Swiss2021 = 8703000

# print out mean +/- sd for the last year
for mat in ["LDPE","HDPE","PP","PS","EPS","PVC","PET"]:
    print("")
    print("Data for "+mat+":")
    
    data = Cons[mat][:,nperiods-1]
    print("- Consumption: "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')
    
    data = Stock[mat][:,nperiods-1]
    print("- In-use stock: "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')
    
    data = Elim[mat][:,nperiods-1]
    print("- Elimination: "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')
    
    data = Lf[mat][:,nperiods-1]
    print("- Landfill: "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')
    
    data = Rs[mat][:,nperiods-1]
    print("- Roadside(macro): "+ str(round(np.mean(data),3))+' ± '+str(round(np.std(data),3))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,6))+' ± '+str(round(np.std(data)/Swiss2021*100000,6))+' kg/cap)')

    data = Sub[mat][:,nperiods-1]
    print("- Sub-surface(micro): "+ str(round(np.mean(data),3))+' ± '+str(round(np.std(data),3))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,6))+' ± '+str(round(np.std(data)/Swiss2021*100000,6))+' kg/cap)')

    data = Asoilma[mat][:,nperiods-1]
    print("- Agri soil(macro): "+ str(round(np.mean(data),3))+' ± '+str(round(np.std(data),3))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,6))+' ± '+str(round(np.std(data)/Swiss2021*100000,6))+' kg/cap)')

    data = Asoilmi[mat][:,nperiods-1]
    print("- Agri soil(micro): "+ str(round(np.mean(data),3))+' ± '+str(round(np.std(data),3))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,6))+' ± '+str(round(np.std(data)/Swiss2021*100000,6))+' kg/cap)')

    data = Nsoilma[mat][:,nperiods-1]
    print("- Natural Soil(macro): "+ str(round(np.mean(data),3))+' ± '+str(round(np.std(data),3))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,6))+' ± '+str(round(np.std(data)/Swiss2021*100000,6))+' kg/cap)')

    data = Nsoilmi[mat][:,nperiods-1]
    print("- Natural Soil(micro): "+ str(round(np.mean(data),3))+' ± '+str(round(np.std(data),3))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,6))+' ± '+str(round(np.std(data)/Swiss2021*100000,6))+' kg/cap)')

    data = Rsoilma[mat][:,nperiods-1]
    print("- Resi soil(macro): "+ str(round(np.mean(data),3))+' ± '+str(round(np.std(data),3))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,6))+' ± '+str(round(np.std(data)/Swiss2021*100000,6))+' kg/cap)')

    data = Rsoilmi[mat][:,nperiods-1]
    print("- Resi soil(micro): "+ str(round(np.mean(data),3))+' ± '+str(round(np.std(data),3))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,6))+' ± '+str(round(np.std(data)/Swiss2021*100000,6))+' kg/cap)')

    data = SWatma[mat][:, nperiods - 1]
    print("- Surface Water(macro): " + str(round(np.mean(data), 3)) + ' ± ' + str(round(np.std(data), 3)) + ' kt (' + str(round(np.mean(data) / Swiss2021 * 100000, 6)) + ' ± ' + str(round(np.std(data) / Swiss2021 * 100000, 6)) + ' kg/cap)')

    data = SWatmi[mat][:, nperiods - 1]
    print("- Surface Water(micro): " + str(round(np.mean(data), 3)) + ' ± ' + str(round(np.std(data), 3)) + ' kt (' + str(round(np.mean(data) / Swiss2021 * 100000, 6)) + ' ± ' + str(round(np.std(data) / Swiss2021 * 100000, 6)) + ' kg/cap)')

    data = Rec[mat][:,nperiods-1]
    print("- Recycling and reuse: "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')
    
    data = RecExp[mat]
    print("- Export of recyclable material: "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')
    
    data = Export[mat]
    print("- Other exports: "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')
    
    print("")
    
    data = (Stock[mat][:,nperiods-1] + Elim[mat][:,nperiods-1] + Lf[mat][:,nperiods-1]  + Rec[mat][:,nperiods-1] + RecExp[mat] + Export[mat])
    print("=> Total (excl. cons): "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')
    


print("")
print("Data for all materials:")

data = (Cons["LDPE"][:,nperiods-1]+
        Cons["HDPE"][:,nperiods-1]+
        Cons["PP"][:,nperiods-1]+
        Cons["PS"][:,nperiods-1]+
        Cons["EPS"][:,nperiods-1]+
        Cons["PVC"][:,nperiods-1]+
        Cons["PET"][:,nperiods-1])
print("- Consumption: "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')

data = (Stock["LDPE"][:,nperiods-1]+
        Stock["HDPE"][:,nperiods-1]+
        Stock["PP"][:,nperiods-1]+
        Stock["EPS"][:,nperiods-1]+
        Stock["PS"][:,nperiods-1]+
        Stock["PVC"][:,nperiods-1]+
        Stock["PET"][:,nperiods-1])
print("- In-use stock: "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')

data = (Elim["LDPE"][:,nperiods-1]+
        Elim["HDPE"][:,nperiods-1]+
        Elim["PP"][:,nperiods-1]+
        Elim["PS"][:,nperiods-1]+
        Elim["EPS"][:,nperiods-1]+
        Elim["PVC"][:,nperiods-1]+
        Elim["PET"][:,nperiods-1])
print("- Elimination: "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')

data = (Lf["LDPE"][:,nperiods-1]+
        Lf["HDPE"][:,nperiods-1]+
        Lf["PP"][:,nperiods-1]+
        Lf["PS"][:,nperiods-1]+
        Lf["EPS"][:,nperiods-1]+
        Lf["PVC"][:,nperiods-1]+
        Lf["PET"][:,nperiods-1])
print("- Landfill: "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')

data = (Rec["LDPE"][:,nperiods-1]+
        Rec["HDPE"][:,nperiods-1]+
        Rec["PP"][:,nperiods-1]+
        Rec["PS"][:,nperiods-1]+
        Rec["EPS"][:,nperiods-1]+
        Rec["PVC"][:,nperiods-1]+
        Rec["PET"][:,nperiods-1])
print("- Recycling and reuse: "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')

data = (RecExp["LDPE"]+
        RecExp["HDPE"]+
        RecExp["PP"]+
        RecExp["PS"]+
        RecExp["EPS"]+
        RecExp["PVC"]+
        RecExp["PET"])
print("- Export of recyclable material: "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')

data = (Export["LDPE"]+
        Export["HDPE"]+
        Export["PP"]+
        Export["PS"]+
        Export["EPS"]+
        Export["PVC"]+
        Export["PET"])
print("- Other exports: "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')

print("")

data = (Stock["LDPE"][:,nperiods-1] + Elim["LDPE"][:,nperiods-1] + Lf["LDPE"][:,nperiods-1] + Rec["LDPE"][:,nperiods-1] + RecExp["LDPE"] + Export["LDPE"] +
        Stock["HDPE"][:,nperiods-1] + Elim["HDPE"][:,nperiods-1] + Lf["HDPE"][:,nperiods-1] + Rec["HDPE"][:,nperiods-1] + RecExp["HDPE"] + Export["HDPE"] +
        Stock["PP"][:,nperiods-1] + Elim["PP"][:,nperiods-1] + Lf["PP"][:,nperiods-1] + Rec["PP"][:,nperiods-1] + RecExp["PP"] + Export["PP"] +
        Stock["PS"][:,nperiods-1] + Elim["PS"][:,nperiods-1] + Lf["PS"][:,nperiods-1] + Rec["PS"][:,nperiods-1] + RecExp["PS"] + Export["PS"] +
        Stock["EPS"][:,nperiods-1] + Elim["EPS"][:,nperiods-1] + Lf["EPS"][:,nperiods-1] + Rec["EPS"][:,nperiods-1] + RecExp["EPS"] + Export["EPS"] +
        Stock["PVC"][:,nperiods-1] + Elim["PVC"][:,nperiods-1] + Lf["PVC"][:,nperiods-1] + Rec["PVC"][:,nperiods-1] + RecExp["PVC"] + Export["PVC"] +
        Stock["PET"][:,nperiods-1] + Elim["PET"][:,nperiods-1] + Lf["PET"][:,nperiods-1] + Rec["PET"][:,nperiods-1] + RecExp["PET"] + Export["PET"])
print("=> Total (excl. cons): "+ str(round(np.mean(data),2))+' ± '+str(round(np.std(data),2))+' kt (' + str(round(np.mean(data)/Swiss2021*100000,3))+' ± '+str(round(np.std(data)/Swiss2021*100000,3))+' kg/cap)')
