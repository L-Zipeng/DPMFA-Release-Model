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

for mat in ["LDPE","HDPE","PP","PS","EPS","PVC","PET"]:
    
    # list all files with inflows for mat
    listfiles = glob.glob(r'.\csv\loggedInflows_'+mat+'*.csv')
    
    unc = np.zeros((len(listfiles),73))
    flonames = []
    
    for j in range(0,len(listfiles)):
        file = listfiles[j]
        data = genfromtxt(file, delimiter=' ')
        flonames.append(file.split("_")[4].split(".")[0])
        
        for i in range(0,np.shape(data)[1]):
            MEAN = np.mean(data[:,i])
            if(MEAN < 0.0000001):
                unc[j,i] = float('nan')
            else:
                unc[j,i] = np.std(data[:,i])/MEAN
    
    years = [str(1950+k) for k in np.arange(0,np.shape(data)[1])]
    
    fig, ax = plt.subplots(figsize=(20,20))
    im = ax.imshow(unc)

    # show all ticks
    ax.set_yticks(np.arange(len(flonames)))
    ax.set_xticks(np.arange(73))
    ax.set_yticklabels(flonames)
    ax.set_xticklabels([str(1950+k) for k in np.arange(0,np.shape(data)[1])])

    ax.set_ylim([-0.5,len(flonames)-0.5])

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(73):
        for j in range(len(listfiles)):
            if not math.isnan(unc[j,i]):
                text = ax.text(i,j, int(round(unc[j,i]*100)),
                               ha="center", va="center", color="w")

    ax.set_title("Relative uncertainty of inflows per compartment and year (STD/MEAN) for "+mat)
    fig.tight_layout()
    plt.show()

    fig.savefig(r'.\Figures\UncertaintyHeatmap_'+mat+'.pdf', bbox_inches='tight')
