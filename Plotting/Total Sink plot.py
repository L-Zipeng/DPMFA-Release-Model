import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import csv


def read_sink_data(file_path):
    """Read and convert sink data to floats, skip non-convertible rows."""
    data = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                # Convert each value in the row to float and multiply by 1000
                data.append([float(val) * 1000 for val in row])
            except ValueError:
                # Skip rows that cannot be converted to float
                continue
    return np.array(data, dtype=np.float32)


def plot_subfigure_for_material(ax, material, target_name, base_folder, start_year):
    # Adjust the pattern to include leading and trailing underscores for exact matches
    # This helps distinguish between "PS" and "EPS"
    if material in ['PS', 'EPS']:
        pattern = os.path.join(base_folder, f"sinks_{material}_{target_name}.csv")
    else:
        pattern = os.path.join(base_folder, f"sinks_{material}_{target_name}.csv")

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

    ax.set_title(material)
    ax.set_xlabel('Year')
    ax.set_ylabel('Flow mass (t)')
    ax.legend(loc='upper left', fontsize='small', framealpha=0.5)
    ax.set_xlim(left=1950)
    ax.set_ylim(bottom=0)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)
    return True


# Prepare the plotting environment
fig, axs = plt.subplots(2, 4, figsize=(20, 10), constrained_layout=True)

# Define parameters
target_names = ["Agricultural Soil (macro)",  "Residential Soil (macro)",
                 "Natural Soil (macro)", "Road Side (macro)","Surface Water (macro)"]
#"Agricultural Soil (micro)","Residential Soil (micro)","Natural Soil (micro)","Sub-surface (micro)", "Surface Water (micro)",

materials = ["LDPE", "HDPE", "PS", "EPS", "PP", "PVC", "PET"]
base_folder = r".\Sinks"  # Adjust this path
start_year = 1950

for target_name in target_names:
    fig, axs = plt.subplots(2, 4, figsize=(20, 10), constrained_layout=True)
    for i, mat in enumerate(materials):
        row = i // 4
        col = i % 4
        if not plot_subfigure_for_material(axs[row, col], mat, target_name, base_folder, start_year):
            fig.delaxes(axs[row, col])  # Delete the axis if no data

plt.show()