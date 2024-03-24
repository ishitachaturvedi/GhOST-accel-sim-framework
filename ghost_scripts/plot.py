import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
import numpy as np
from pathlib import Path
import pandas as pd

plt.rcParams['font.style'] = 'normal'
plt.rcParams['font.family'] = 'serif'  # Use a generic family
font = {'family': 'Times New Roman', 'color':  'black', 'weight': 'normal', 'size': 20}
print(matplotlib.get_cachedir())
# exit(0)

def read_csv(csv_file) -> pd.DataFrame:
    """Read a CSV file and return a DataFrame."""
    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip()
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip()
    return df

def is_geo(benchmark):
    geomean_names = ("GEOMEAN", "geomean", "mean", "MEAN", "Geomean", "Mean", "geometric mean", "Geometric mean", 'Geo', 'GEO', 'geo')
    return benchmark in geomean_names


def get_color(idx=0):
    # colors = ['#0D95D0', '#7DC462', '#E72F52', '#774FA0', '#EFB743', '#D44627']
    colors = ['#6C8EBF', '#81B365', '#9773A6','#F2AF29',  '#B95451']
    # colors = ['#6C8EBF', '#81B365', '#9773A6','#D79B02', '#D6B656', '#B95451']
    # colors = ['#DAE8FC', '#D6E8D5', '#FFE6CC', '#E1D5E7', '#FFF2CC', '#F8CECC']
    return colors[idx % len(colors)]


def get_text_color(idx=0):
    colors = ['#21437f', '#3c6b2a', '#54276e', '#825913', '#15342b', '#D44627']
    # colors = ['#6C8EBF', '#81B365', '#9773A6','#F2AF29',  '#3B5249', '#B95451']
    # colors = ['#6C8EBF', '#81B365', '#9773A6','#D79B02', '#D6B656', '#B95451']
    # colors = ['#DAE8FC', '#D6E8D5', '#FFE6CC', '#E1D5E7', '#FFF2CC', '#F8CECC']
    return colors[idx % len(colors)]

class BenchmarkManager:
    _instance = None
    rename = {
        "slurm-convolution_reduced.out": "slurm-convolution.out",
        "convolution": "slurm-convolution.out",
        "LavaMD": "slurm-lavaMD_rodinia.out",
    }

    def __new__(cls, benchmark_csv):
        if cls._instance is None:
            cls._instance = super(BenchmarkManager, cls).__new__(cls)
            cls._instance._init(benchmark_csv)
        return cls._instance

    def _init(self, benchmark_csv):
        # Read the CSV file
        benchmark_df = read_csv(benchmark_csv)

        # Store the DataFrame and create a benchmarks dictionary
        self.benchmark_df = benchmark_df
        self.benchmarks = {row['Benchmark']: {'suite': row['Suite'], 'short': row['Short']}
                           for _, row in benchmark_df.iterrows()}
    
    def rename_check(self, benchmark):
        if benchmark in self.rename:
            return self.rename[benchmark]
        return benchmark

    def get_benchmark_all(self):
        """List all benchmarks."""
        return list(self.benchmarks.keys())

    def get_benchmarks(self, suite):
        """List all benchmarks in a specific suite."""
        return [b for b, info in self.benchmarks.items() if info['suite'] == suite]

    def get_suite(self, benchmark):
        """Find the suite for a specific benchmark."""
        benchmark = self.rename_check(benchmark)
        return self.benchmarks.get(benchmark, {}).get('suite')

    def short_to_benchmark(self, short_name):
        """Find benchmark by short name."""
        return next((b for b, info in self.benchmarks.items() if info['short'] == short_name), None)

    def benchmark_to_short(self, benchmark):
        """Parse short name of a benchmark."""
        benchmark = self.rename_check(benchmark)
        return self.benchmarks.get(benchmark, {}).get('short')


def plot_fig_3(bm: BenchmarkManager, directory : Path, input_file: Path):
    output_pdf = directory / (input_file.stem + '.pdf')
    output_png = directory / (input_file.stem + '.png')
    
    # Read the CSV file into a DataFrame
    # df = pd.read_csv(input_file, index_col=0)  # Assuming the first column is an index column

    # # Strip spaces from string columns (both keys and values)
    # df.columns = df.columns.str.strip()
    # for col in df.select_dtypes(['object']).columns:  # Applies only to string columns
    #     df[col] = df[col].str.strip()
    
    df = read_csv(input_file)
    val = df.astype(int).to_dict(orient='list')

    line_styles = ['-', '--', '-.', ':', (0, (3, 5, 1, 5)), (0, (5, 10))]

    plt.hist(val["1440"], bins=100,alpha = 1, linestyle=line_styles[0], color="orange", histtype='step',label="1")
    plt.hist(val["976"], bins=100,alpha = 1, linestyle=line_styles[1], color="green", histtype='step',label="2")
    plt.hist(val["1232"], bins=100,alpha = 1, linestyle=line_styles[2], color="red", histtype='step',label="3")
    plt.hist(val["992"], bins=100,alpha = 1, linestyle=line_styles[3], color="blue", histtype='step',label="4")
    plt.hist(val["1472"], bins=100,alpha = 1, linestyle=line_styles[4], color="black", histtype='step',label="6")
    plt.hist(val["1248"], bins=100,alpha = 1, linestyle=line_styles[5], color="grey", histtype='step',label="9")
    plt.yscale("log")
    plt.xlabel('Latency (Cycles)',fontdict=font)
    plt.ylabel('Frequency',fontdict=font)
    legend = plt.legend(title='PC')
    plt.tight_layout()
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    
    print(f"Saving plot to {output_pdf} and {output_png}")
    plt.savefig(output_pdf, bbox_inches='tight')
    plt.savefig(output_png, bbox_inches='tight')


def plot_fig_13(bm: BenchmarkManager, directory : Path, input_file: Path):
    output_pdf = directory / (input_file.stem + '.pdf')
    output_png = directory / (input_file.stem + '.png')

    # Assuming the BenchmarkManager class is defined as before and includes the get_benchmark_all method

    # Load the perfectOOO.csv file
    fig_13_csv = read_csv(input_file)

    # Prepare the data for plotting
    plot_data = []
    for _, row in fig_13_csv.iterrows():
        benchmark = row['Benchmark']
        sched_stalls = fig_13_csv[fig_13_csv['Benchmark'] == benchmark]['IBOOO_8_sched'].values[0]
        values = [row['IBOOO_8'], row['IBOOO_8_occupancy'], sched_stalls]
        for i, v in enumerate(values):
            if v == 2:
                values[i] = 0
                print(f"Found 2: {benchmark} {i} {v}")
        if is_geo(benchmark):
            short_name = "GEO"
            suite_name = "~GEO"
        else:
            try:
                short_name = bm.benchmark_to_short(benchmark)
                suite_name = bm.get_suite(benchmark)
            except KeyError:
                print(f"KeyError: {benchmark}")
                continue
        plot_data.append((short_name, values, suite_name))

    # Sort plot data by suite name for better grouping in the plot
    plot_data.sort(key=lambda x: x[2])

    # Separate data into components for plotting
    short_names, values, suite_names = zip(*plot_data)
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)
    fig = plt.figure(figsize=(20, 3.6))
    plt.rc("font", family="Times New Roman")
    ax_len = 3
    ax = fig.add_subplot(1,1,1)
    ay = ax.twinx()
    ending = 0.15
    sep = 0.05
    wid = (1 - ending * 2 - sep * (ax_len - 1)) / ax_len
    plot_values = list(zip(*values))
    bars = ay.bar(np.array(range(len(values))) - (0.5 - ending) + (wid + sep) * 2 + wid / 2, list(zip(*values))[1], wid , color=get_color(0), label = "Occupancy")
    bars = ay.bar(np.array(range(len(values))) - (0.5 - ending) + (wid + sep) * 1 + wid / 2, 100 * (np.array(list(zip(*values))[2]) - 1), wid , color=get_color(3), label = "Scheduler Stall Reduced")
    # for i, v in enumerate(plot_values):
    bars = ax.bar(np.array(range(len(values))) - (0.5 - ending) + (wid + sep) * 0 + wid / 2, np.array(list(zip(*values))[0]) - 1, wid , color=get_color(1), label = "Ghost", bottom=1)

    # Add suite names below the x-axis
    ax.set_xticks(ticks=range(len(short_names)))
    ax.set_xticklabels(short_names, rotation=45, ha='center', fontsize=18)
    ax.set_xlim(-0.5, len(short_names) - 0.5)

    # Annotate suite names
    current_suite = plot_data[0][2]
    begin_idx = 0
    for idx, (short, _, suite) in enumerate(plot_data):
        if suite != current_suite:
            ax.axvline(x=idx - 0.5, color='lightgray', linestyle='--')
            ax.text((begin_idx + idx - 1) / 2, 0.90, f"{current_suite}", ha='center', va='center', 
                    fontsize=18)
            
            # print(f"{current_suite} ({begin_idx}, {idx})")
            current_suite = suite
            begin_idx = idx

    for (idx, v) in enumerate(list(zip(*values))[0]):
        if v > 1.2:
            ax.text((idx - 0.7), 1.195, f"{v:.2f}", ha='center', va='top', 
                    fontsize=16, color="green")

    for (idx, v) in enumerate(list(zip(*values))[2]):
        if v > 1.2:
            ay.text((idx + 0.5), 19.5, f"{100 * (v -1):.0f}%", ha='center', va='top', 
                    fontsize=16, color="brown")

    for (idx, v) in enumerate(list(zip(*values))[1]):
        if v > 20:
            if idx != len(values) - 1:
                ay.text((idx + 0.70), 19.5, f"{v:.0f}%", ha='center', va='top', 
                        fontsize=16, color="darkblue")
            else:
                ay.text((idx - 0.2), 19.5, f"{v:.0f}%", ha='center', va='top', 
                        fontsize=16, color="darkblue")  
    # Adding labels and title
    # ax.yticks(fontsize=20)
    ax.set_ylabel('Speedup', size=20)
    ax.tick_params(axis='y', labelsize=20)
    ax.set_ylim(1, 1.2)
    ax.grid(axis='y')

    ay.set_ylim(0, 2)
    ay.set_ylabel('Stall Reduced (%)\n& Occupancy (%)', size=20)
    ay.tick_params(axis='y', labelsize=20)
    ay.set_yticks([0, 10, 20])
    fig.legend(
        ncol=3,
        bbox_to_anchor=[0.94, 0.86],
        loc='upper right',
        prop={"size": 20},
        borderaxespad=0.1,
        labelspacing=0.25,
        handlelength=0.75,
        handletextpad=0.25,
        borderpad=0.15,
    )

    # Show the plot
    plt.tight_layout()
    print(f"Saving plot to {output_pdf} and {output_png}")
    plt.savefig(output_pdf, bbox_inches='tight')
    plt.savefig(output_png, bbox_inches='tight')

def plot_fig_14(bm: BenchmarkManager, directory : Path, input_file: Path):
    output_pdf = directory / (input_file.stem + '.pdf')
    output_png = directory / (input_file.stem + '.png')

    ghostprecise_df = read_csv(input_file)

    ib_sizes = [str(2 * 2 ** (i + 1)) for i in range(4)]
    # Prepare the data for plotting
    plot_data = []
    for _, row in ghostprecise_df.iterrows():
        benchmark = row['Benchmark']
        values = [float(row[ib]) for ib in ib_sizes]
        # If the value is exactly 2, set it to 0
        for i, v in enumerate(values):
            if v > 2:
                values[i] = 1
                print(f"Found 2: {benchmark} {i} {v}")
        if is_geo(benchmark):
            short_name = "GEO"
            suite_name = "~GEO"
        else:
            try:
                short_name = bm.benchmark_to_short(benchmark)
                suite_name = bm.get_suite(benchmark)
            except KeyError:
                print(f"KeyError: {benchmark}")
                continue
        plot_data.append((short_name, values, suite_name))


    # Sort plot data by suite name for better grouping in the plot
    plot_data.sort(key=lambda x: x[2])

    # Separate data into components for plotting
    short_names, values, suite_names = zip(*plot_data)
    # Plotting
    plt.figure(figsize=(20, 3.6))
    plt.rc("font", family="Times New Roman")
    ax_len = len(values[0])
    ending = 0.1
    sep = 0.04
    wid = (1 - ending * 2 - sep * (ax_len - 1)) / ax_len
    for i, v in enumerate(zip(*values)):
        bars = plt.bar(np.array(range(len(v))) - (0.5 - ending) + (wid + sep) * i + wid / 2, np.array(v) - 1, wid , color=get_color(i), label = ib_sizes[i], bottom=1)

    # Add suite names below the x-axis
    plt.xticks(rotation=45, ha='center', fontsize=18)
    plt.gca().xaxis.set_major_locator(ticker.FixedLocator(range(len(short_names))))
    plt.gca().xaxis.set_major_formatter(ticker.FixedFormatter(short_names))
    plt.xlim(-0.5, len(short_names) - 0.5)

    # Annotate suite names
    current_suite = plot_data[0][2]
    begin_idx = 0
    for idx, (short, _, suite) in enumerate(plot_data):
        if suite != current_suite:
            plt.axvline(x=idx - 0.5, color='gray', linestyle='--')
            plt.gca().text((begin_idx + idx - 1) / 2, 0.7, f"{current_suite}", ha='center', va='center', 
                        fontsize=18)
            current_suite = suite
            begin_idx = idx

    # Adding labels and title
    plt.yticks(fontsize=20)
    plt.ylabel('Speedup', size=20)
    plt.ylim(0.88, 1.4)
    plt.grid(axis='y')

    plt.legend(
        ncol=len(ib_sizes),
        bbox_to_anchor=[0.65, 0.88],
        loc='center',
        prop={"size": 20},
        borderaxespad=0.1,
        labelspacing=0.25,
        handlelength=0.75,
        handletextpad=0.25,
        borderpad=0.15,
    )

    # Show the plot
    plt.tight_layout()
    print(f"Saving plot to {output_pdf} and {output_png}")
    plt.savefig(output_pdf, bbox_inches='tight')
    plt.savefig(output_png, bbox_inches='tight')

def plot_fig_15(bm: BenchmarkManager, directory : Path, input_file: Path):
    output_pdf = directory / (input_file.stem + '.pdf')
    output_png = directory / (input_file.stem + '.png')
    
    data_df = read_csv(input_file)

    ib_sizes = [str(2 * 2 ** (i + 1)) for i in range(4)]

    for _, row in data_df.iterrows():
        if not is_geo(row['Benchmark']):
            continue
        values_2060 = [float(row[f'IBOOO_{ib_sizes[s]}']) for s in range(len(ib_sizes))]
        values_3070 = [float(row[f'IBOOO_{ib_sizes[s]}_RTX3070']) for s in range(len(ib_sizes))]

    values = [values_2060, values_3070]

    # Plotting
    plt.figure(figsize=(10, 2.4))
    plt.rc("font", family="Times New Roman")
    ax_len = len(values[0])
    ending = 0.2
    sep = 0.025
    wid = (1 - ending * 2 - sep * (ax_len - 1)) / ax_len

    for i, v in enumerate(zip(*values)):
        bars = plt.bar(np.array(range(len(v))) - (0.5 - ending) + (wid + sep) * i + wid / 2, np.array(v) - 1, wid , color=get_color(i), label = ib_sizes[i], bottom=1)

    # Add suite names below the x-axis
    plt.xticks(rotation=0, ha='center', fontsize=18)
    short_names = ["RTX 2060S", "RTX 3070"]
    plt.gca().xaxis.set_major_locator(ticker.FixedLocator(range(len(short_names))))
    plt.gca().xaxis.set_major_formatter(ticker.FixedFormatter(short_names))
    plt.xlim(-0.8, len(values) - 0.2)
    plt.yticks(fontsize=20)
    plt.ylabel('Speedup', size=20)
    plt.ylim(1, 1.08)
    plt.grid(axis='y')

    plt.legend(
        ncol=len(ib_sizes),
        bbox_to_anchor=[0.65, 0.88],
        loc='center',
        prop={"size": 20},
        borderaxespad=0.1,
        labelspacing=0.25,
        handlelength=0.75,
        handletextpad=0.25,
        borderpad=0.15,
    )
    plt.subplots_adjust(bottom=0.1)

    # Show the plot
    plt.tight_layout()
    print(f"Saving plot to {output_pdf} and {output_png}")
    plt.savefig(output_pdf, bbox_inches='tight')
    plt.savefig(output_png, bbox_inches='tight')

def plot_fig_16(bm: BenchmarkManager, directory : Path, input_file: Path):
    
    output_pdf = directory / (input_file.stem + '.pdf')
    output_png = directory / (input_file.stem + '.png')
    
    data_df = read_csv(input_file)

    # Prepare the data for plotting
    ib_sizes = [str(2 ** (i + 1)) for i in range(5)]
    plot_data = []
    
    for _, row in data_df.iterrows():
        if not is_geo(row['Benchmark']):
            continue
        for k, v in (row.to_dict().items()):
            if k == 'Benchmark':
                continue
            plot_data.append((k, [v], "GEO"))

    # Plotting
    ax_len = 3
    plt.figure(figsize=(10, 2.4))
    plt.rc("font", family="Times New Roman")
    ending = 0.24
    sep = 0.05
    wid = (1 - ending * 2 - sep * (ax_len - 1)) / ax_len
    for i, (policy, v, _) in enumerate(plot_data):
        bars = plt.bar(np.array(range(len(v))) - (0.5 - ending) + (wid + sep) * i + wid / 2, np.array(v) - 1, wid , color=get_color(i), label = policy, bottom=1)

    # Add suite names below the x-axis
    plt.xticks(rotation=0, ha='center', fontsize=18)
    plt.xlim(-0.5, 0.5)
    plt.xticks([0], ["GEO"])
    
    # Annotate suite names
    current_suite = plot_data[0][2]
    begin_idx = 0
    for idx, (short, _, suite) in enumerate(plot_data):
        if suite != current_suite:
            plt.axvline(x=idx - 0.5, color='gray', linestyle='--')
            plt.gca().text((begin_idx + idx - 1) / 2, 0.73, f"{current_suite}", ha='center', va='center', 
                        fontsize=18)
            current_suite = suite
            begin_idx = idx

    plt.yticks(fontsize=20)
    plt.ylabel('Speedup', size=20)
    plt.grid(axis='y')

    plt.legend(
        ncol=len(ib_sizes),
        bbox_to_anchor=[0.35, 0.88],
        loc='center',
        prop={"size": 20},
        borderaxespad=0.1,
        labelspacing=0.25,
        handlelength=0.75,
        handletextpad=0.25,
        borderpad=0.15,
    )
    plt.subplots_adjust(bottom=0.1)
    # Show the plot
    plt.tight_layout()
    print(f"Saving plot to {output_pdf} and {output_png}")
    plt.savefig(output_pdf, bbox_inches='tight')
    plt.savefig(output_png, bbox_inches='tight')

def plot_fig_17(bm: BenchmarkManager, directory : Path, input_file: Path):

    output_pdf = directory / (input_file.stem + '.pdf')
    output_png = directory / (input_file.stem + '.png')
    
    # Load the perfectOOO.csv file
    ghostloogoccup_df = read_csv(input_file)

    # Prepare the data for plotting
    plot_data = []
    plot_data_geo = []
    exclude = ["slurm-LIB.out"]
    for _, row in ghostloogoccup_df.iterrows():
        benchmark = row['Benchmark']
        if benchmark in exclude: # exclude LIB benchmark
            continue
        values = [row['IBOOO_8'], row['LOOG_OoO']]
        
        # If the value is exactly 2, set it to 0
        for i, v in enumerate(values):
            if v == 2:
                values[i] = 0
                print(f"Found 2: {benchmark} {i} {v}")

        # Append the short name, perfect OoO value, and suite name
        if is_geo(benchmark):
            short_name = "GEO"
            suite_name = "~GEO"
            # plot_data_geo.append((short_name, values, suite_name))
        else:
            try:
                short_name = bm.benchmark_to_short(benchmark)
                suite_name = bm.get_suite(benchmark)
            except KeyError:
                print(f"KeyError: {benchmark}")
                continue
            plot_data.append((short_name, values, suite_name))

    # recalculate the GEOMEAN
    _, values, __ = zip(*plot_data)
    (ghost_values, loog_values) = zip(*values)
    geo_ghost = np.prod(ghost_values) ** (1 / len(ghost_values))
    geo_loog = np.prod(loog_values) ** (1 / len(loog_values))
    plot_data_geo.append(("GEO", (geo_ghost, geo_loog), "~GEO"))

    # Sort plot data by suite name for better grouping in the plot
    plot_data.sort(key=lambda x: x[2])
    short_names, values, suite_names = zip(*plot_data)
    # Plotting
    fig = plt.figure(figsize=(20, 4.25))
    plt.rc("font", family="Times New Roman")
    ax_len = len(values[0])
    ax = fig.add_subplot(1,1,1)
    # ay = ax.twinx()

    top = 1.3
    bottom = 0.7
    ending = 0.15
    sep = 0.05
    wid = (1 - ending * 2 - sep * (ax_len - 1)) / ax_len
    plot_values = list(zip(*values))[:2]
    # bars = ay.bar(np.array(range(len(values))) - (0.5 - ending) + (wid + sep) * 2 + wid / 2, list(zip(*values))[2], wid , color=get_color(0), label = "Occupancy")
    length = len(values)
    for i, v in enumerate(plot_values):
        # bars = ax.bar(np.array(range(len(v))) + i * (length), np.array(v) - 1, wid  , color=get_color(i + 1), label = ("GhOST", "LOOG")[i], bottom=1)
        bars = ax.bar(np.array(range(len(v))) + i * (length), np.array(v) - 1, wid * 2  , color=get_color(i + 1), label = ("GhOST", "LOOG")[i], bottom=1)
    short_names_geo, values_geo, suite_names_geo = zip(*plot_data_geo)
    bars = ax.bar(2 * (length) - (0.5 - ending) + wid / 2, values_geo[0][0] - 1, wid * 1.35, color=get_color(1), bottom=1)
    bars = ax.bar(2 * (length) - (0.5 - ending) + wid / 2 + 1 * (sep + wid), values_geo[0][1] - 1, wid * 1.35, color=get_color(2), bottom=1)

    # Add suite names below the x-axis
    ax.set_xticks(ticks=range(len(short_names) * 2 + 1))
    ax.set_xticklabels([x + "   " for x in short_names] + [x + "   " for x in short_names] + ['GEO',], rotation=50, ha='center', fontsize=18)
    ax.set_xlim(-0.5, len(short_names) * 2 + 1 - 0.5)

    # Annotate suite names
    current_suite = plot_data[0][2]
    begin_idx = 0
    for suite_i in range(2):
        for idx, (short, _, suite) in enumerate(plot_data):
            idx += suite_i * len(short_names)
            if suite != current_suite:
                ax.axvline(x=idx - 0.5, color='gray', linestyle='--')
                ax.text((begin_idx + idx - 1) / 2, 0.48, f"{current_suite}", ha='center', va='top', 
                        fontsize=18)  
                current_suite = suite
                begin_idx = idx
    ax.text((begin_idx + idx - 1) / 2, 0.48, f"{current_suite}", ha='center', va='top', 
                        fontsize=18)  
    ax.axvline(x=idx + 0.5, color='gray', linestyle='--')

    ghost_color = "green"
    loog_color = "#432251"

    for (idx, v) in enumerate(list((plot_values))[0]):
        if v > top:
            ax.text((idx + 0.69), 1.29, f"{v:.2f}", ha='center', va='top', 
                    fontsize=16, color=ghost_color)
        if v < bottom:
            ax.text((idx + 0.08), 0.67, f"{v:.2f}", ha='center', va='top', 
                    fontsize=16, color=ghost_color)
            
    for (idx, v) in enumerate(list((plot_values))[1]):
        idx += len(plot_values[0])
        if v > top:
            ax.text((idx + 0.69), 1.29, f"{v:.2f}", ha='center', va='top', 
                    fontsize=16, color=loog_color)
        if v < bottom:
            ax.text((idx + 0.08), 0.67, f"{v:.2f}", ha='center', va='top', 
                    fontsize=16, color=loog_color)



    # Adding labels and title
    plt.yticks(fontsize=20)
    ax.set_ylabel('Speedup', size=20)
    ax.set_ylim(bottom, top)
    ax.grid(axis='y')
    ax.axhline(y=1.0, color='#444', linestyle='--')

    fig.legend(
        ncol=2,
        bbox_to_anchor=[0.512, 0.882],
        loc='center',
        prop={"size": 20},
        borderaxespad=0.1,
        labelspacing=0.25,
        handlelength=0.75,
        handletextpad=0.25,
        borderpad=0.15,
    )
    # Show the plot
    plt.tight_layout()
    print(f"Saving plot to {output_pdf} and {output_png}")
    plt.savefig(output_pdf, bbox_inches='tight')
    plt.savefig(output_png, bbox_inches='tight')


def plot_fig_19(bm: BenchmarkManager, directory : Path, input_file: Path):

    output_pdf = directory / (input_file.stem + '.pdf')
    output_png = directory / (input_file.stem + '.png')
    # Load the perfectOOO.csv file
    ghostloogoccup_df = read_csv(input_file)

    # Prepare the data for plotting
    plot_data = []
    geo_values = []
    min_values = [10000, 10000]
    max_values = [-1, -1]
    exclude = ["slurm-LIB.out"]
    for _, row in ghostloogoccup_df.iterrows():
        benchmark = row['Benchmark']
        if benchmark in exclude: # exclude LIB benchmark
            continue
        values = [row['IBOOO_8'], row['LOOG_OoO']]
        
        for i, v in enumerate(values):
            if v == 2:
                values[i] = 0
                print(f"Found 2: {benchmark} {i} {v}")

        # Append the short name, perfect OoO value, and suite name
        if is_geo(benchmark):
            short_name = "GEO"
            suite_name = "~GEO"
            
            geo_values = values
        else:
            try:
                short_name = bm.benchmark_to_short(benchmark)
                suite_name = bm.get_suite(benchmark)
            except KeyError:
                print(f"KeyError: {benchmark}")
                continue
            plot_data.append((short_name, values, suite_name))
            min_values = [min(min_values[i], values[i]) for i in range(len(values))]
            max_values = [max(max_values[i], values[i]) for i in range(len(values))]

    # recalculate the GEOMEAN
    _, values, __ = zip(*plot_data)
    (ghost_values, loog_values) = zip(*values)
    geo_ghost = np.prod(ghost_values) ** (1 / len(ghost_values))
    geo_loog = np.prod(loog_values) ** (1 / len(loog_values))
    geo_values = [geo_ghost, geo_loog]

    # Sort plot data by suite name for better grouping in the plot
    plot_data.sort(key=lambda x: x[2])

    # Separate data into components for plotting
    short_names, values, suite_names = zip(*plot_data)
    # print(short_names, perfect_ooos, suite_names)

    # Plotting
    fig = plt.figure(figsize=(16, 6))
    plt.rc("font", family="Times New Roman")
    ax_len = len(values[0])
    ax = fig.add_subplot(1,2,1)
    ay = fig.add_subplot(1,2,2)
    # ay = ax.twinx()
    ending = 0.15
    sep = 0.05
    wid = (1 - ending * 2 - sep * (ax_len - 1)) / ax_len
    plot_values = list(zip(*values))[:2]
    ax.ecdf(plot_values[0],  color=get_color(1), linestyle='-', linewidth=2)
    ax.ecdf(plot_values[1], color=get_color(2), linestyle='-', linewidth=2)


    fontsize = 28

    # # Adding labels and title
    ax.set_xlabel('Speedup', size=fontsize)
    ax.tick_params(axis='x', labelsize=fontsize)
    ax.tick_params(axis='y', labelsize=fontsize)
    ax.set_ylabel('CDF', size=fontsize)
    ax.set_ylim(0, 1)
    ax.grid(axis='both')
    ax.axvline(x=1.0, color='black', linestyle='-', linewidth=1)


    # ay = ax.twinx()
    ay_len = 2
    ending = 0.2
    sep = 0.1
    wid = (1 - ending * 2 - sep * (ay_len - 1)) / ay_len
    top = 1.5
    plot_values = list(zip(min_values, max_values, geo_values))
    for i, v in enumerate(plot_values):
        bars = ay.bar(np.array(range(len(v))) - (0.5 - ending) + (wid + sep) * i + wid / 2, np.array(v) - 1, wid , color=get_color(i + 1), label = ("GhOST", "LOOG")[i], bottom=1)
        for j, value in enumerate(v):
            ay.text(j - (0.5 - ending) + (wid + sep) * i + wid / 2, min(top + 0.05, value + 0.05) if value > 1 else value - 0.06, f"{value:.2f}", ha='center', va='center', color=get_text_color(i + 1),
                    fontsize=fontsize + 1)

    ay.set_xticks([0, 1, 2])
    ay.set_xticklabels(["MIN", "MAX", "GEO"], size=fontsize)
    ay.tick_params(axis='x', labelsize=fontsize)
    ay.tick_params(axis='y', labelsize=fontsize)
    ay.set_ylabel('Speedup', size=fontsize)
    ay.set_ylim(0.2, top)
    ay.grid(axis='both')
    ay.axhline(y=1.0, color='black', linestyle='-', linewidth=1)

    fig.legend(
        ncol=2,
        bbox_to_anchor=[0.77, 0.19],
        loc='center',
        prop={"size": fontsize},
        borderaxespad=0.1,
        labelspacing=0.25,
        handlelength=0.75,
        handletextpad=0.25,
        borderpad=0.15,
    )
    # Show the plot
    plt.tight_layout()
    print(f"Saving plot to {output_pdf} and {output_png}")
    plt.savefig(output_pdf, bbox_inches='tight')
    plt.savefig(output_png)


if __name__ == "__main__":
    
    data_csv = {
        "fig_3": "fig_3.csv",
        "fig_13": "fig_13.csv",
        "fig_14": "fig_14.csv",
        "fig_15": "fig_15.csv",
        "fig_16": "fig_16.csv",
        "fig_17": "fig_17.csv",
        "fig_19": "fig_19.csv",
    }
    
    plot_funcs = {
        "fig_3": plot_fig_3,
        "fig_13": plot_fig_13,
        "fig_14": plot_fig_14,
        "fig_15": plot_fig_15,
        "fig_16": plot_fig_16,
        "fig_17": plot_fig_17,
        "fig_19": plot_fig_19
    }
    
    directory = Path(__file__).parent
    if (str(directory).split("/")[-1] == "ghost_scripts"):
        directory = directory.parent
    outfile_folder = directory / "results"
    outfile_folder.mkdir(exist_ok=True)
    
    # Examatplotlibe usage:
    benchmark_csv = directory / "ghost_scripts" / 'benchmarks.csv'
    bm = BenchmarkManager(benchmark_csv)
    
    print("Current directory: ", directory, ", output folder: ", outfile_folder)
    for name, file in data_csv.items():
        print(f"Running {name} with {outfile_folder / file}")
        plot_funcs[name](bm, outfile_folder, input_file=outfile_folder / file)
        print("\n")

