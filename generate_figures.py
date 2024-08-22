import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import inspect
from tqdm import tqdm
import pandas as pd

# Constants setup
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['axes.labelsize'] = 16
mpl.rcParams['text.usetex'] = True

OUT_DIR = "./figures/"
DPI = 300
FIG_HEIGHT = 3.1
FIG_WIDTH = 6
X_TICK_LABELS_FONT_SIZE = 12
LEGEND_FONT_SIZE = 12

# Colorblind-friendly colors
colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']

def fig_2():
    # Example data for papers
    papers = {
        '2020': {'ICSE': 0, 'FSE': 0, 'ISSTA': 0, 'ASE': 0},
        '2021': {'ICSE': 0, 'FSE': 1, 'ISSTA': 0, 'ASE': 0},
        '2022': {'ICSE': 1, 'FSE': 0, 'ISSTA': 1, 'ASE': 1},
        '2023': {'ICSE': 5, 'FSE': 1, 'ISSTA': 3, 'ASE': 2},
        '2024\n(until July)': {'ICSE': 5, 'FSE': 1, 'ISSTA': 2, 'ASE': 0},
    }

    # Initialize plot data
    years = sorted(papers.keys())
    conferences = ['ICSE', 'FSE', 'ISSTA', 'ASE']
    hatches = ['/', '\\', '|', '-']

    # Create stacked bar plot
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))

    bottom = np.zeros(len(years))

    for i, conf in enumerate(conferences):
        values = [papers[year][conf] for year in years]
        ax.bar(years, values, label=conf, bottom=bottom, color=colors[i % len(colors)], hatch=hatches[i])
        bottom += np.array(values)

    # Set labels and title
    ax.set_xlabel('Year', fontsize=X_TICK_LABELS_FONT_SIZE)
    ax.set_ylabel('Number of Papers', fontsize=X_TICK_LABELS_FONT_SIZE)

    # Adjust tick label size
    ax.tick_params(axis='both', which='major', labelsize=X_TICK_LABELS_FONT_SIZE)

    # Add legend
    ax.legend(fontsize=LEGEND_FONT_SIZE, loc='upper left', frameon=False)
    
    fig.tight_layout(pad=0.02)

    figname = inspect.stack()[0][3]
    plt.savefig("{}{}.pdf".format(OUT_DIR, figname), dpi=DPI, format="pdf")

def fig_3():
    # Example data for dataset usage
    datasets = {
        'BigVul': 16,
        'Devign': 14,
        'ReVeal': 10,
        'D2A': 2,
        'SARD': 2,
        'NVD': 1,
        'CodeReviewer': 1,
        'Defects4J': 1,
        'CVEFixes': 1,
        'DeepWukong': 1,
        'Self Collected': 1,
    }

    # Initialize plot data
    dataset_names = list(datasets.keys())
    usage_counts = list(datasets.values())

    # Create bar plot
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))

    ax.bar(dataset_names, usage_counts, color=colors[:len(dataset_names)])

    # Set labels and title
    ax.set_xlabel('Datasets', fontsize=X_TICK_LABELS_FONT_SIZE)
    ax.set_ylabel('Number of Papers', fontsize=X_TICK_LABELS_FONT_SIZE)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Adjust tick label size
    ax.tick_params(axis='both', which='major', labelsize=X_TICK_LABELS_FONT_SIZE)

    fig.tight_layout(pad=0.02)

    figname = inspect.stack()[0][3]
    plt.savefig("{}{}.pdf".format(OUT_DIR, figname), dpi=DPI, format="pdf")
    
def fig_4():
    # Example data for papers
    papers = {
        '2020': {'Devign': 27, 'BigVul': 0, 'DiverseVul': 0},
        '2021': {'Devign': 82, 'BigVul': 16, 'DiverseVul': 0},
        '2022': {'Devign': 165, 'BigVul': 37, 'DiverseVul': 0},
        '2023': {'Devign': 323, 'BigVul': 111, 'DiverseVul': 14},
        '2024\n(until July)': {'Devign': 165, 'BigVul': 76, 'DiverseVul': 54},
    }

    # Initialize plot data
    years = sorted(papers.keys())
    conferences = ['Devign', 'BigVul', 'DiverseVul']
    hatches = ['/', '\\', '|', '-']

    # Create stacked bar plot
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))

    bottom = np.zeros(len(years))

    for i, conf in enumerate(conferences):
        values = [papers[year][conf] for year in years]
        ax.bar(years, values, label=conf, bottom=bottom, color=colors[i % len(colors)], hatch=hatches[i])
        bottom += np.array(values)

    # Set labels and title
    ax.set_xlabel('Year', fontsize=X_TICK_LABELS_FONT_SIZE)
    ax.set_ylabel('Number of Citations', fontsize=X_TICK_LABELS_FONT_SIZE)

    # Adjust tick label size
    ax.tick_params(axis='both', which='major', labelsize=X_TICK_LABELS_FONT_SIZE)

    # Add legend
    ax.legend(fontsize=LEGEND_FONT_SIZE, loc='upper left', frameon=False)
    
    fig.tight_layout(pad=0.02)

    figname = inspect.stack()[0][3]
    plt.savefig("{}{}.pdf".format(OUT_DIR, figname), dpi=DPI, format="pdf")

def fig_6():
    
    def count_lines_of_code(functions):
        return [len(func.split('\n')) for func in functions]

    # Load the datasets
    bigvul_data = pd.read_csv('raw_samples/bigvul_sample.csv')
    diversevul_data = pd.read_csv('raw_samples/diversevul_sample.csv')
    devign_data = pd.read_csv('raw_samples/devign_sample.csv')

    # Extract the functions and count lines of code
    bigvul_lines = count_lines_of_code(bigvul_data['func_before'])
    diversevul_lines = count_lines_of_code(diversevul_data['func'])
    devign_lines = count_lines_of_code(devign_data['func'])

    # Create stacked bar plot
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))

    # Generate the box plots
    data_to_plot = [bigvul_lines, diversevul_lines, devign_lines]
    ax.boxplot(data_to_plot, showfliers=False)
    
    # Set labels and title
    ax.set_ylabel('Lines of Code', fontsize=X_TICK_LABELS_FONT_SIZE)
    
     # Set the labels for the x-axis
    ax.set_xticklabels(['BigVul', 'DiverseVul', 'Devign'], fontsize=X_TICK_LABELS_FONT_SIZE)

    # Adjust tick label size
    ax.tick_params(axis='both', which='major', labelsize=X_TICK_LABELS_FONT_SIZE)

    # Add legend
    ax.legend(fontsize=LEGEND_FONT_SIZE, loc='upper center', frameon=False,ncol=2)
    
    fig.tight_layout(pad=0.02)

    figname = inspect.stack()[0][3]
    plt.savefig("{}{}.pdf".format(OUT_DIR, figname), dpi=DPI, format="pdf")
    
def main():
    fig_functions = [
        fig_2,
        fig_3,
        fig_4,
        fig_6,
    ]
    
    progress_bar = tqdm(range(len(fig_functions)))
    
    for func in fig_functions:
        func()
        progress_bar.update(1)

if __name__ == '__main__':
    main()