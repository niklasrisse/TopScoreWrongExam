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

def fig_2a():
    # Updated mapping: 4 now represents the merged "Line/Statement" (former 4 and 6)
    number_to_label = {
        1: "Function",
        2: "File",
        3: "Inter-procedural Slice",
        4: "Line/Statement",  # merged from previous keys 4 and 6
        5: "Repository",
        7: "Program",
        8: "Commit",
        9: "Multiple Functions"
    }
    
    # Load CSV file
    df = pd.read_csv('literature_survey_data.csv', delimiter=";")
    
    # Filter rows based on the given conditions
    filtered_df = df[(df["Software Vulnerability Detection?"] == "Yes") & 
                     (df["Machine Learning?"] == "Yes")]
    
    # Extract granularities and conference information
    granularities = filtered_df["Granularities"].dropna().str.split(',')
    conference_data = filtered_df["Conference"]
    granularity_counts = {}
    conference_counts = {}

    # Initialize conference categories
    conference_categories = {
        "SE Conferences": ["ICSE", "FSE", "ISSTA", "ASE"],
        "Journals": ["TSE", "TOSEM", "TIFS", "TDSC"],
        "Security Conferences": ["SP", "CCS", "USENIX", "NDSS"],
    }

    # Process granularities and conferences
    for i, gran_list in enumerate(granularities):
        # Convert items to integers and merge granularity 4 and 6 into 4.
        # Using a set ensures each paper counts only once for the merged granularity.
        processed_grans = set()
        for gran in gran_list:
            gran_int = int(gran)
            if gran_int in [4, 6]:
                processed_grans.add(4)
            else:
                processed_grans.add(gran_int)
                
        for gran in processed_grans:
            if gran not in granularity_counts:
                granularity_counts[gran] = {key: 0 for key in conference_categories.keys()}
            for conf_cat, conf_names in conference_categories.items():
                if any(conf in conference_data.iloc[i] for conf in conf_names):
                    granularity_counts[gran][conf_cat] += 1

    # Calculate total number of papers
    total_papers = filtered_df.shape[0]

    # Sort granularities by total count (descending order)
    sorted_counts = sorted(granularity_counts.items(), 
                           key=lambda x: sum(x[1].values()), 
                           reverse=True)
    labels = [number_to_label[k] for k, _ in sorted_counts]
    values = [v for _, v in sorted_counts]

    # Reverse the order for top-to-bottom sorting in horizontal bar chart
    labels.reverse()
    values.reverse()

    # Extract conference-wise data
    se_counts = [v["SE Conferences"] for v in values]
    journal_counts = [v["Journals"] for v in values]
    security_counts = [v["Security Conferences"] for v in values]

    # Create the figure and plot
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    bar_width = 0.8

    # Define colors and hatch patterns
    se_color, journal_color, security_color = colors[:3]
    se_bars = ax.barh(labels, se_counts, color=se_color, label="SE Conferences", height=bar_width)
    journal_bars = ax.barh(labels, journal_counts, color=journal_color, label="Journals", height=bar_width,
                           left=se_counts, hatch="///")
    security_bars = ax.barh(labels, security_counts, color=security_color, label="Security Conferences", 
                            height=bar_width, left=[i + j for i, j in zip(se_counts, journal_counts)], hatch="xx")

    # Add absolute numbers and percentages to the end of each bar
    for label, total, se, journal, security in zip(labels, 
                                                   [sum(d.values()) for d in values], 
                                                   se_counts, 
                                                   journal_counts, 
                                                   security_counts):
        percentage = (total / total_papers) * 100
        ax.text(total + 1, labels.index(label), f"{total} ({percentage:.1f}\%)", va='center', fontsize=X_TICK_LABELS_FONT_SIZE)

    # Set labels and ticks
    ax.set_xlabel('Number of Papers', fontsize=X_TICK_LABELS_FONT_SIZE)
    ax.set_ylabel('Granularity', fontsize=X_TICK_LABELS_FONT_SIZE)
    ax.tick_params(axis='both', which='major', labelsize=X_TICK_LABELS_FONT_SIZE)

    # Add legend in the bottom-right corner
    ax.legend(loc='lower right', fontsize=X_TICK_LABELS_FONT_SIZE, frameon=False)

    # Adjust layout to give more space on the right for numbers and percentages
    ax.set_xlim(0, max(sum(d.values()) for d in values) + max(sum(d.values()) for d in values) * 0.3)
    fig.tight_layout(pad=0.02)

    # Save the figure
    figname = inspect.stack()[0][3]
    plt.savefig(f"{OUT_DIR}{figname}.pdf", dpi=DPI, format="pdf")
    
def fig_2b():
    # Load CSV file
    df = pd.read_csv('literature_survey_data.csv', delimiter=";")
    
    # Filter rows based on the given conditions
    filtered_df = df[(df["Software Vulnerability Detection?"] == "Yes") & 
                     (df["Machine Learning?"] == "Yes")]
    
    # Extract conference information and year
    conference_data = filtered_df["Conference"]
    years = filtered_df["Year"].astype(int)
    
    # Initialize conference categories
    conference_categories = {
        "SE Conferences": ["ICSE", "FSE", "ISSTA", "ASE"],
        "Journals": ["TSE", "TOSEM", "TIFS", "TDSC"],
        "Security Conferences": ["SP", "CCS", "USENIX", "NDSS"],
    }

    # Initialize a dictionary to count papers per year and per category
    year_range = range(years.min(), years.max() + 1)
    paper_counts = {year: {cat: 0 for cat in conference_categories.keys()} for year in year_range}

    # Populate counts
    for year, confs in zip(years, conference_data):
        for conf_cat, conf_names in conference_categories.items():
            if any(conf in confs for conf in conf_names):
                paper_counts[year][conf_cat] += 1

    # Prepare data for plotting
    years = sorted(paper_counts.keys())
    categories = conference_categories.keys()
    hatches = [None, "///", "xx"]
    
    # Initialize plot
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    bottom = np.zeros(len(years))
    
    for i, category in enumerate(categories):
        values = [paper_counts[year][category] for year in years]
        ax.bar(years, values, label=category, bottom=bottom, color=colors[i % len(colors)], hatch=hatches[i])
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
    plt.savefig(f"{OUT_DIR}{figname}.pdf", dpi=DPI, format="pdf")

def fig_3updated():
    datasets = {
        1: "Devign",
        2: "ReVeal",
        3: "BigVul",
        4: "DiverseVul",
        5: "D2A",
        6: "SARD",
        7: "NVD",
        8: "CodeReviewer",
        9: "Defects4J",
        10: "CVEFixes",
        11: "DeepWukong",
        12: "Self Collected",
        13: "Asterisk",
        14: "OpenSSL",
        15: "CWE119",
        16: "CWE399",
        17: "CWE416",
        18: "Juliet",
        19: "Draper",
        20: "s-Babi",
        21: "wireshark",
        22: "CG Database",
        23: "RealVul",
        24: "FUNDED",
        25: "9 projects",
        26: "Android",
        27: "Firefox",
        28: "CVAD",
        29: "SVulD",
        30: "CrossVul",
    }

    # Load the CSV file
    df = pd.read_csv('literature_survey_data.csv', delimiter=";")
    
    # Extract and process the "Dataset" column
    dataset_col = df["Datasets"].dropna().str.split(',')
    dataset_counts = {}

    for dataset_list in dataset_col:
        for dataset_id in map(int, dataset_list):
            dataset_name = datasets[dataset_id]
            dataset_counts[dataset_name] = dataset_counts.get(dataset_name, 0) + 1

    # Group datasets with a count of 1 under "Other"
    grouped_counts = {"Other": 0}
    for dataset, count in dataset_counts.items():
        if count == 1:
            grouped_counts["Other"] += 1
        else:
            grouped_counts[dataset] = count

    # Sort datasets by frequency (descending)
    grouped_counts = dict(sorted(grouped_counts.items(), key=lambda x: x[1], reverse=True))

    # Prepare data for plotting
    labels = list(grouped_counts.keys())
    values = list(grouped_counts.values())

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    bars = ax.bar(labels, values, color=colors[:len(labels)])  # Use colors from the colors array

    # Add absolute numbers above each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, str(int(height)), 
                ha='center', va='bottom', fontsize=X_TICK_LABELS_FONT_SIZE)

    # Set x-axis labels and rotate them
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=X_TICK_LABELS_FONT_SIZE)

    # Set labels and title
    ax.set_xlabel('Dataset', fontsize=X_TICK_LABELS_FONT_SIZE)
    ax.set_ylabel('Number of Papers', fontsize=X_TICK_LABELS_FONT_SIZE)
    ax.tick_params(axis='y', which='major', labelsize=X_TICK_LABELS_FONT_SIZE)

    # Adjust layout with more space at the top
    ax.set_ylim(0, max(values) + max(values) * 0.2)  # Add 20% extra space at the top
    fig.tight_layout(pad=0.02)

    # Save the figure
    figname = inspect.stack()[0][3]
    plt.savefig(f"{OUT_DIR}{figname}.pdf", dpi=DPI, format="pdf")
    
def fig_4updated():
    # Example data for papers
    papers = {
        '2020': {'Devign': 27, 'BigVul': 0, 'DiverseVul': 0},
        '2021': {'Devign': 82, 'BigVul': 16, 'DiverseVul': 0},
        '2022': {'Devign': 165, 'BigVul': 37, 'DiverseVul': 0},
        '2023': {'Devign': 323, 'BigVul': 111, 'DiverseVul': 14},
        '2024': {'Devign': 404, 'BigVul': 204, 'DiverseVul': 100},
    }

    # Initialize plot data
    years = sorted(papers.keys())
    conferences = ['Devign', 'BigVul', 'DiverseVul']
    hatches = ['/', '\\', '|', '-']

    # Create stacked bar plot
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT * 0.8))

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
    
def main():
    fig_functions = [
        fig_2a,
        fig_2b,
        fig_3updated,
        fig_4updated,
    ]
    
    progress_bar = tqdm(range(len(fig_functions)))
    
    for func in fig_functions:
        func()
        progress_bar.update(1)

if __name__ == '__main__':
    main()