# -*- coding: utf-8 -*-
"""

"""

import os
import pandas as pd
import numpy as np
import glob
from numpy import genfromtxt
import matplotlib.pyplot as plt

### Stocks ####################################################################

listfiles = glob.glob(r'./csv/stocks_LDPE*.csv')
LDPE = np.zeros((10000, 73))
for file in listfiles:
    temp = genfromtxt(file, delimiter=' ')
    LDPE = LDPE + temp

listfiles = glob.glob(r'./csv/stocks_HDPE*.csv')
HDPE = np.zeros((10000, 73))
for file in listfiles:
    temp = genfromtxt(file, delimiter=' ')
    HDPE = HDPE + temp

listfiles = glob.glob(r'./csv/stocks_PP*.csv')
PP = np.zeros((10000, 73))
for file in listfiles:
    temp = genfromtxt(file, delimiter=' ')
    PP = PP + temp

listfiles = glob.glob(r'./csv/stocks_PS*.csv')
PS = np.zeros((10000, 73))
for file in listfiles:
    temp = genfromtxt(file, delimiter=' ')
    PS = PS + temp

listfiles = glob.glob(r'./csv/stocks_EPS*.csv')
EPS = np.zeros((10000, 73))
for file in listfiles:
    temp = genfromtxt(file, delimiter=' ')
    EPS = EPS + temp

listfiles = glob.glob(r'./csv/stocks_PVC*.csv')
PVC = np.zeros((10000, 73))
for file in listfiles:
    temp = genfromtxt(file, delimiter=' ')
    PVC = PVC + temp

listfiles = glob.glob(r'./csv/stocks_PET*.csv')
PET = np.zeros((10000, 73))
for file in listfiles:
    temp = genfromtxt(file, delimiter=' ')
    PET = PET + temp

mytitle = 'Consumption stocks'

nperiods = np.shape(LDPE)[1]
nsim = np.shape(LDPE)[0]

startYear = 1950
endYear = 2022
xScale = np.arange(startYear, startYear + nperiods)

colors = ['darkred', 'red', 'orange', 'gold', 'yellowgreen', 'teal', 'mediumorchid']

### Calculate mean and SD #######################################################

def compute_stats(data):
    mean = [np.mean(data[:,i]) for i in range(data.shape[1])]
    sd = [np.std(data[:,i]) for i in range(data.shape[1])]
    return mean, sd

meanLDPE, sdLDPE = compute_stats(LDPE)
meanHDPE, sdHDPE = compute_stats(HDPE)
meanPP, sdPP = compute_stats(PP)
meanPS, sdPS = compute_stats(PS)
meanEPS, sdEPS = compute_stats(EPS)
meanPVC, sdPVC = compute_stats(PVC)
meanPET, sdPET = compute_stats(PET)


fig = plt.figure('stock')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Flow mass (kt)', fontsize=14)
plt.title(mytitle)
plt.rcParams['font.size'] = 12  # tick's font
plt.xlim(xmin=startYear - 0.5, xmax=startYear + nperiods - 0.5)

# Plot
def plot_with_sd(x, mean, sd, color, label):
    plt.plot(x, mean, color=color, linewidth=2, label=label)
    plt.fill_between(x, np.subtract(mean, sd), np.add(mean, sd), color=color, alpha=0.3)

plot_with_sd(xScale, meanLDPE, sdLDPE, colors[0], 'LDPE')
plot_with_sd(xScale, meanHDPE, sdHDPE, colors[1], 'HDPE')
plot_with_sd(xScale, meanPP, sdPP, colors[2], 'PP')
plot_with_sd(xScale, meanPS, sdPS, colors[3], 'PS')
plot_with_sd(xScale, meanEPS, sdEPS, colors[4], 'EPS')
plot_with_sd(xScale, meanPVC, sdPVC, colors[5], 'PVC')
plot_with_sd(xScale, meanPET, sdPET, colors[6], 'PET')

plt.ylim(0, 1700)
plt.legend(loc='upper left', fontsize='small')
plt.tight_layout()


fig.savefig(r'.\Figures\Stock_with_SD.pdf', bbox_inches='tight')

# figure (cumulative)
fig = plt.figure('stock_cum')
plt.xlabel('Year',fontsize=14)
plt.ylabel('Flow mass (kt)',fontsize=14)
plt.title(mytitle)
plt.rcParams['font.size']=12 # tick's font
plt.xlim(xmin=startYear-0.5, xmax=startYear+nperiods-0.5)
zeroes = [0 for t in xScale]
intermsum0 = meanLDPE
intermsum1 = [sum(x) for x in zip(intermsum0, meanHDPE)]
intermsum2 = [sum(x) for x in zip(intermsum1, meanPP)]
intermsum3 = [sum(x) for x in zip(intermsum2, meanPS)]
intermsum4 = [sum(x) for x in zip(intermsum3, meanEPS)]
intermsum5 = [sum(x) for x in zip(intermsum4, meanPVC)]
intermsum6 = [sum(x) for x in zip(intermsum5, meanPET)]
plt.fill_between(xScale, zeroes,     intermsum0, color = colors[0], linewidth=0, label='LDPE')
plt.fill_between(xScale, intermsum0, intermsum1, color = colors[1], linewidth=0, label='HDPE')
plt.fill_between(xScale, intermsum1, intermsum2, color = colors[2], linewidth=0, label='PP')
plt.fill_between(xScale, intermsum2, intermsum3, color = colors[3], linewidth=0, label='PS')
plt.fill_between(xScale, intermsum3, intermsum4, color = colors[4], linewidth=0, label='EPS')
plt.fill_between(xScale, intermsum4, intermsum5, color = colors[5], linewidth=0, label='PVC')
plt.fill_between(xScale, intermsum5, intermsum6, color = colors[6], linewidth=0, label='PET')
plt.ylim(0, 5000)
plt.legend(loc='upper left', fontsize = 'small')
plt.tight_layout()
fig.savefig(r'.\Figures\Stock_cum.pdf', bbox_inches='tight')

### Consumption ###############################################################

# get list of product categories
data = pd.read_excel(os.path.join(r".\Compartments.xlsx"),
                     sheet_name="Rank")

pclist = []
for i in np.arange(0, data.shape[0]):
    if data.loc[i, :][2] == "Stock":
        pclist.append(data.loc[i, :][1])

listfiles = glob.glob(r'./csv/loggedInflows_LDPE*.csv')
listfiles = [t for t in listfiles if any([n in t for n in pclist])]
LDPE = np.zeros((10000, 73))
for file in listfiles:
    temp = genfromtxt(file, delimiter=' ')
    LDPE = LDPE + temp

listfiles = glob.glob(r'./csv/loggedInflows_HDPE*.csv')
listfiles = [t for t in listfiles if any([n in t for n in pclist])]
HDPE = np.zeros((10000, 73))
for file in listfiles:
    temp = genfromtxt(file, delimiter=' ')
    HDPE = HDPE + temp

listfiles = glob.glob(r'./csv/loggedInflows_PP*.csv')
listfiles = [t for t in listfiles if any([n in t for n in pclist])]
PP = np.zeros((10000, 73))
for file in listfiles:
    temp = genfromtxt(file, delimiter=' ')
    PP = PP + temp

listfiles = glob.glob(r'./csv/loggedInflows_PS*.csv')
listfiles = [t for t in listfiles if any([n in t for n in pclist])]
PS = np.zeros((10000, 73))
for file in listfiles:
    temp = genfromtxt(file, delimiter=' ')
    PS = PS + temp

listfiles = glob.glob(r'./csv/loggedInflows_EPS*.csv')
listfiles = [t for t in listfiles if any([n in t for n in pclist])]
EPS = np.zeros((10000, 73))
for file in listfiles:
    temp = genfromtxt(file, delimiter=' ')
    EPS = EPS + temp

listfiles = glob.glob(r'./csv/loggedInflows_PVC*.csv')
listfiles = [t for t in listfiles if any([n in t for n in pclist])]
PVC = np.zeros((10000, 73))
for file in listfiles:
    temp = genfromtxt(file, delimiter=' ')
    PVC = PVC + temp

listfiles = glob.glob(r'./csv/loggedInflows_PET*.csv')
listfiles = [t for t in listfiles if any([n in t for n in pclist])]
PET = np.zeros((10000, 73))
for file in listfiles:
    temp = genfromtxt(file, delimiter=' ')
    PET = PET + temp

mytitle = 'Yearly consumption'

nperiods = np.shape(LDPE)[1]
nsim = np.shape(LDPE)[0]

startYear = 1950
endYear = 2022
xScale = np.arange(startYear, startYear + nperiods)

colors = ['darkred', 'red', 'orange', 'gold', 'yellowgreen', 'teal', 'mediumorchid']
def compute_stats(data):
    mean = [np.mean(data[:,i]) for i in range(data.shape[1])]
    sd = [np.std(data[:,i]) for i in range(data.shape[1])]
    return mean, sd

meanLDPE, sdLDPE = compute_stats(LDPE)
meanHDPE, sdHDPE = compute_stats(HDPE)
meanPP, sdPP = compute_stats(PP)
meanPS, sdPS = compute_stats(PS)
meanEPS, sdEPS = compute_stats(EPS)
meanPVC, sdPVC = compute_stats(PVC)
meanPET, sdPET = compute_stats(PET)

## plot #############################################

fig = plt.figure('consumption')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Flow mass (kt)', fontsize=14)
plt.title(mytitle)
plt.rcParams['font.size'] = 12
plt.xlim(xmin=startYear - 0.5, xmax=startYear + nperiods - 0.5)

plot_with_sd(xScale, meanLDPE, sdLDPE, colors[0], 'LDPE')
plot_with_sd(xScale, meanHDPE, sdHDPE, colors[1], 'HDPE')
plot_with_sd(xScale, meanPP, sdPP, colors[2], 'PP')
plot_with_sd(xScale, meanPS, sdPS, colors[3], 'PS')
plot_with_sd(xScale, meanEPS, sdEPS, colors[4], 'EPS')
plot_with_sd(xScale, meanPVC, sdPVC, colors[5], 'PVC')
plot_with_sd(xScale, meanPET, sdPET, colors[6], 'PET')

plt.ylim(0, 400)
plt.legend(loc='upper left', fontsize='small')
plt.tight_layout()

fig.savefig(r'.\Figures\Con_with_SD.pdf', bbox_inches='tight')





