import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import csv


def plot_subfigure_for_material(ax, material, target_name, base_folder, start_year):
    # Adjust the pattern to include leading and trailing underscores for exact matches
    # This helps distinguish between "PS" and "EPS"
    if material in ['PS', 'EPS']:
        pattern = os.path.join(base_folder, f"*_{material}_*_to_{target_name}.csv")
    else:
        pattern = os.path.join(base_folder, f"*{material}_*_to_{target_name}.csv")

    files = glob.glob(pattern)

    if not files:  # Skip if no files found for the target
        return False

    colors = plt.cm.viridis(np.linspace(0, 1, len(files)))

    for file, color in zip(files, colors):
        with open(file, 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            data = np.array([[float(val) * 1000 for val in row] for row in reader if row], dtype=np.float32)

        if data.size > 0:
            mean_flow = np.mean(data, axis=0)
            sd_flow = np.std(data, axis=0)
            percentile_25 = np.percentile(data, 25, axis=0)
            percentile_75 = np.percentile(data, 75, axis=0)

            x_scale = np.arange(start_year, start_year + len(mean_flow))
            compartment_name = os.path.basename(file).split('_')[2]

            ax.plot(x_scale, mean_flow, label=compartment_name, color=color, linewidth=2, alpha=0.8)
            ax.plot(x_scale, percentile_25, '--', color=color, alpha=0.5)
            ax.plot(x_scale, percentile_75, '--', color=color, alpha=0.5)
            ax.fill_between(x_scale, mean_flow - sd_flow, mean_flow + sd_flow, color=color, alpha=0.2)

    ax.set_title(f'{material} to {target_name}')
    ax.set_xlabel('Year')
    ax.set_ylabel('Flow mass (t)')
    ax.legend(loc='upper left', fontsize='small', framealpha=0.2)
    ax.set_xlim(left=1950, right=2022)
    ax.set_ylim(bottom=0)
    ax.grid(True, which='both', linewidth=0.5, alpha=0.5)
    return True


# Define your target names and other parameters
target_names = ["Surface Water (macro)"]
#"Agricultural Soil (macro)", "Agricultural Soil (micro)", "Residential Soil (macro)","Residential Soil (micro)", "Natural Soil (macro)", "Natural Soil (micro)", "Sub-surface (micro)", "Surface Water (micro)", "Surface Water (macro)", "Road Side (macro)"
materials = ["LDPE", "HDPE", "PS", "EPS", "PP", "PVC", "PET"]
base_folder = r".\Outflow"  # Adjust this path
start_year = 1950

# Loop over each target name and save figures
for target_name in target_names:
    fig, axs = plt.subplots(2, 4, figsize=(20, 10), constrained_layout=True)
    for i, mat in enumerate(materials):
        row = i // 4
        col = i % 4
        plot_subfigure_for_material(axs[row, col], mat, target_name, base_folder, start_year)

        # Hide any unused subplots (in case of a grid that's not fully populated)
    for i in range(len(materials), axs.size):
        fig.delaxes(axs.flatten()[i])

    # Adjust figure title to include the target name
    fig.suptitle(target_name, fontsize=16)

    # Save figure with a high resolution
    figure_filename = os.path.join(r".\Figures", f"{target_name}.jpg")
    plt.savefig(figure_filename, format='jpg', dpi=300)
    plt.close() 
