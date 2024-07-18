
import numpy as np
import glob
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from math import log10, floor
import pandas as pd

startYear = 1950
endYear = 2022
nPeriods = endYear-startYear+1
nSIM = 10000
xScale = np.arange(startYear,startYear+nPeriods)

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
      
      "Automotive","Mobility Textiles",
        
      "Electrical and Electronic Equipment",
        
      "Household Plastics",
      "Furniture",
      "Fabric Coatings",
      "Personal Care and Cosmetic Products",
      "Other Plastic Products",
           
      "Clothing", "Technical Clothing",
          
      "Household Textiles",
      "Technical Household Textiles",
            
      "Hygiene and Medical Textiles",
      "Other Technical Textiles"]

# import all the stock data
Stocks = {}
for mat in ["LDPE","HDPE","PP","PS","EPS","PVC","PET"]:
    Stocks[mat] = []
    listfiles = glob.glob(r'.\csv\stocks_'+mat+'*.csv')
    
    for comp in pc:
        file = r'.\csv\stocks_'+mat+'_'+comp+'.csv'
        
        if file in listfiles:
            temp = genfromtxt(file, delimiter=' ')
            Stocks[mat].append(np.mean(temp[:,np.shape(temp)[1]-1]))
        else:
            Stocks[mat].append(0)

# import all the consumption data
Cons = {}
for mat in ["LDPE","HDPE","PP","PS","EPS","PVC","PET"]:
    Cons[mat] = []
    listfiles = glob.glob(r'.\csv\loggedInflows_'+mat+'*.csv')
    
    for comp in pc:
        file = r'.\csv\loggedInflows_'+mat+'_'+comp+'.csv'
        
        if file in listfiles:
            temp = genfromtxt(file, delimiter=' ')
            Cons[mat].append(np.mean(temp[:,np.shape(temp)[1]-1]))
        else:
            Cons[mat].append(0)

# calculate the sum of all stocks
Total =  [sum(x) for x in zip(Stocks["LDPE"], Stocks["HDPE"], Stocks["PP"], Stocks["PS"], Stocks["EPS"], Stocks["PVC"], Stocks["PET"])]
# determine the order of increasing pc
plotorder =  np.argsort(Total)

print(Total)

### figure

fig, axs = plt.subplots(1, 2, figsize=(10,10))
labels  = [pc[t] for t in plotorder]
colors = ['darkred', 'red', 'orange', 'gold', 'yellowgreen', 'teal', 'mediumorchid']

# consumption bar plot
toplot1 = [Cons["LDPE"][t] for t in plotorder]
toplot2 = [Cons["HDPE"][t] for t in plotorder]
toplot3 = [Cons["PP"][t] for t in plotorder]
toplot4 = [Cons["PS"][t] for t in plotorder]
toplot5 = [Cons["EPS"][t] for t in plotorder]
toplot6 = [Cons["PVC"][t] for t in plotorder]
toplot7 = [Cons["PET"][t] for t in plotorder]

interm2 = toplot1
interm3 = [sum(x) for x in zip(toplot1, toplot2)]
interm4 = [sum(x) for x in zip(toplot1, toplot2, toplot3)]
interm5 = [sum(x) for x in zip(toplot1, toplot2, toplot3, toplot4)]
interm6 = [sum(x) for x in zip(toplot1, toplot2, toplot3, toplot4, toplot5)]
interm7 = [sum(x) for x in zip(toplot1, toplot2, toplot3, toplot4, toplot5, toplot6)]

ax = axs[0]
ax.barh(labels, [8 for t in plotorder], color = ["whitesmoke","white"])

ax.barh(labels, toplot1, label='LDPE', color = colors[0])
ax.barh(labels, toplot2, label='HDPE', color = colors[1], left=interm2)
ax.barh(labels, toplot3, label='PP',   color = colors[2], left=interm3)
ax.barh(labels, toplot4, label='PS',   color = colors[3], left=interm4)
ax.barh(labels, toplot5, label='EPS',  color = colors[4], left=interm5)
ax.barh(labels, toplot6, label='PVC',  color = colors[5], left=interm6)
ax.barh(labels, toplot7, label='PET',  color = colors[6], left=interm7)

ax.set_xlim(120, 0)
ax.set_ylim(-0.5, 34.5)
ax.set_xlabel('Mass (kt)')
ax.set_title('Consumption in 2022')

# stock bar plot
toplot1 = [Stocks["LDPE"][t] for t in plotorder]
toplot2 = [Stocks["HDPE"][t] for t in plotorder]
toplot3 = [Stocks["PP"][t] for t in plotorder]
toplot4 = [Stocks["PS"][t] for t in plotorder]
toplot5 = [Stocks["EPS"][t] for t in plotorder]
toplot6 = [Stocks["PVC"][t] for t in plotorder]
toplot7 = [Stocks["PET"][t] for t in plotorder]

interm2 = toplot1
interm3 = [sum(x) for x in zip(toplot1, toplot2)]
interm4 = [sum(x) for x in zip(toplot1, toplot2, toplot3)]
interm5 = [sum(x) for x in zip(toplot1, toplot2, toplot3, toplot4)]
interm6 = [sum(x) for x in zip(toplot1, toplot2, toplot3, toplot4, toplot5)]
interm7 = [sum(x) for x in zip(toplot1, toplot2, toplot3, toplot4, toplot5, toplot6)]

ax = axs[1]
ax.barh(labels, [100 for t in plotorder], color = ["whitesmoke","white"])

ax.barh(labels, toplot1, label='LDPE', color = colors[0])
ax.barh(labels, toplot2, label='HDPE', color = colors[1], left=interm2)
ax.barh(labels, toplot3, label='PP',   color = colors[2], left=interm3)
ax.barh(labels, toplot4, label='PS',   color = colors[3], left=interm4)
ax.barh(labels, toplot5, label='EPS',  color = colors[4], left=interm5)
ax.barh(labels, toplot6, label='PVC',  color = colors[5], left=interm6)
ax.barh(labels, toplot7, label='PET',  color = colors[6], left=interm7)

ax.get_yaxis().set_visible(False)
ax.set_xlim(0, 1800)

ax.set_ylim(-0.5, 34.5)
ax.set_xlabel('Mass (kt)')
ax.set_title('Stock magnitude')
ax.legend(loc='lower right')

fig.subplots_adjust(wspace=0.001)
fig.savefig(r'.\Stocks_by_pc.pdf', bbox_inches='tight')
