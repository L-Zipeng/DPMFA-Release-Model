# -*- coding: utf-8 -*-
"""
"""


import os
import pandas as pd
import numpy as np
import math
import glob
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

pcpack = ["Consumer Films",
          "Consumer Bags",
          "Consumer Bottles",
          "Other Consumer Packaging",
          "Other Non Consumer Films",
          "Non Consumer Bags",
          "Other Non Consumer Packaging"]

pcagri = ["Agricultural Packaging Films",
          "Agricultural Packaging Bottles",
          "Agricultural Films",
          "Agricultural Pipes",
          "Other Agricultural Plastics",
          "Agrotextiles"]

pcbc = ["Building Packaging Films",  
        "Pipes and Ducts",
        "Insulation",
        "Wall and Floor Coverings",
        "Windows, Profiles and Fitted Furniture",
        "Lining",
        "Geotextiles",
        "Building Textiles"]

pcauto = ["Automotive","Mobility Textiles"]

pceee = ["Electrical and Electronic Equipment"]

pcother = ["Household Plastics",
           "Furniture",
           "Fabric Coatings",
           "Personal Care and Cosmetic Products",
           "Other Plastic Products"]

pccloth = ["Clothing", "Technical Clothing"]

pchhtext = ["Household Textiles",
            "Technical Household Textiles"]

pcothertext = ["Hygiene and Medical Textiles",
               "Other Technical Textiles"]

secnames = ["Packaging",
            "Construction",
            "Automotive",
            "Agriculture",
            "EEE",
            "Clothing",
            "Household textiles",
            "Other plastic",
            "Other textile"]

pc = [pcpack,
      pcbc,
      pcauto,
      pcagri,
      pceee,
      pccloth,
      pchhtext,
      pcother,
      pcothertext]

nperiods = 73
startYear = 1950
endYear = 2022
xScale = np.arange(startYear,startYear+nperiods)

colors = ["tomato","dimgrey", "yellow", "aquamarine","mediumvioletred", "indigo","dodgerblue", "yellowgreen", "olive"]

### Cons per sector ####################################################################

fig, axs = plt.subplots(2, 4,figsize=(10,4), sharey=True, sharex=True)
for mat in ["LDPE","HDPE","PP","PS","EPS","PVC","PET"]:
    
    if mat == 'LDPE':
        ax = axs[0,0]
    elif mat == 'HDPE':
        ax = axs[0,1]
    elif mat == 'PP':
        ax = axs[0,2]
    elif mat == 'PS':
        ax = axs[0,3]
    elif mat == 'EPS':
        ax = axs[1,0]
    elif mat == 'PVC':
        ax = axs[1,1]
    elif mat == 'PET':
        ax = axs[1,2]
    
    # list all files with inflows for mat
    listfiles = glob.glob(r'.\loggedInflows_'+mat+'*.csv')
    
    toplot = []
    for sector, pclist in zip(secnames, pc):
        # take those for sector
        tempfiles = [t for t in listfiles if any([n in t for n in pclist])]
        
        data = np.zeros((10000,73))
        for file in tempfiles:
            tempdata = genfromtxt(file, delimiter=' ')
            data = data+tempdata
            
        means = []
        for i in range(0,np.shape(data)[1]):
            tempdata = np.mean(data[:,i])
            if math.isnan(tempdata):
                means.append(0)
            else:
                means.append(tempdata)
        
        toplot.append(means)
    
    if mat == "EPS" or mat == "PVC" or mat == "PET": ax.set_xlabel('Year',fontsize=14)
    if mat == "LDPE" or mat == "EPS": ax.set_ylabel('Mass (kt)',fontsize=14)
    ax.set_title(mat,y=.75)
#    ax.rcParams['font.size']=12 # tick's font
    ax.set_xlim(xmin=startYear-0.5, xmax=startYear+nperiods-0.5)
    ax.stackplot(xScale, toplot, colors=colors, labels=secnames)
#    if mat == "LDPE": ax.legend(loc='upper left', fontsize = 'small')
#    plt.tight_layout()

axs[1,3].axis('off')
patches = [mpatches.Patch(color=colors[0], label=secnames[0]),
           mpatches.Patch(color=colors[1], label=secnames[1]),
           mpatches.Patch(color=colors[2], label=secnames[2]),
           mpatches.Patch(color=colors[3], label=secnames[3]),
           mpatches.Patch(color=colors[4], label=secnames[4]),
           mpatches.Patch(color=colors[5], label=secnames[5]),
           mpatches.Patch(color=colors[6], label=secnames[6]),
           mpatches.Patch(color=colors[7], label=secnames[7]),
           mpatches.Patch(color=colors[8], label=secnames[8])]
axs[1,3].legend(handles=patches, loc='upper left', fontsize = 'small')
fig.suptitle("Yearly consumption in Switzerland", y=1.05)
fig.subplots_adjust(wspace=0,hspace=0)
fig.tight_layout()
fig.savefig(r'\Cons_by_sec.pdf', bbox_inches='tight')
