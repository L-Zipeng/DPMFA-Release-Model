
import os
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt

def read_sink_data(base_path, materials):
    dict_data = {}
    for mat in materials:
        dict_data[mat] = {}
        listfiles = glob.glob(os.path.join(base_path, f'sinks_{mat}*.csv'))
        for sink in ["Export", "Incineration", "Landfill", "Material Reuse",
                     "Textile Reuse", "Automotive Parts Reuse", "Residential Soil (macro)", "Residential Soil (micro)", "Agricultural Soil (macro)", "Agricultural Soil (micro)",
                     "Sub-surface (micro)", "Natural Soil (macro)", "Natural Soil (micro)", "Road Side (macro)", "Surface Water (macro)", "Surface Water (micro)"]:
            file = os.path.join(base_path, f'sinks_{mat}_{sink}.csv')
            if file in listfiles:
                dict_data[mat][sink] = pd.read_csv(file, delimiter=' ').values
            else:
                dict_data[mat][sink] = np.zeros((10000, 73))
    return dict_data

def calculate_shares_and_means(dict_data):
    shares = {}
    means = {}
    for mat, sinks in dict_data.items():
        total = np.sum(list(sinks.values()), axis=0)
        shares[mat] = {sink: value/total for sink, value in sinks.items()}
        means[mat] = {sink: np.nanmean(value, axis=1) for sink, value in sinks.items()}
    return shares, means

def plot_data(means, materials, sinks, title, ylabel, output_path, prefix):
    x_scale = np.arange(1950, 2023)
    colors = ['darkgoldenrod', 'gold', 'limegreen', 'lightblue', 'slategray' ,'darkred', 'red', 'orange', 'gold', 'yellowgreen', 'teal', 'mediumorchid']

    for mat in materials:
        toplot = [means[mat][sink] for sink in sinks]
        plt.figure(figsize=(10, 6))
        plt.stackplot(x_scale, toplot, colors=colors, labels=sinks)
        plt.xlabel('Year', fontsize=14)
        plt.ylabel(ylabel, fontsize=14)
        plt.title(f'{mat} {title} in Switzerland', fontsize=16)
        plt.legend(loc='upper left', fontsize='small')
        plt.tight_layout()
        plt.savefig(os.path.join(output_path, f'{prefix}_{mat}.pdf'), bbox_inches='tight')
        plt.close()

# Usage example:
base_path = r'.\csv'
output_path = r'.\Figures'
materials = ["LDPE", "HDPE", "PP", "PS", "EPS", "PVC", "PET"]

dict_data = read_sink_data(base_path, materials)
shares, means = calculate_shares_and_means(dict_data)

# Example plot for macroplastic in Environmental compartments
sinks_macro = ["Residential Soil (macro)", "Agricultural Soil (macro)", "Natural Soil (macro)", "Road Side (macro)", "Surface Water (macro)"]
plot_data(means, materials, sinks_macro, 'Macroplastic Environmental Sinks', 'Share', output_path, 'Sinks_macro_cum')

# Adjust the `sinks_macro`, `title`, `ylabel`, and `prefix` as needed for other plots
