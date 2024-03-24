from pathlib import Path
from os import chdir, getcwd
import csv
from functools import lru_cache


# Definition of necessary functions for statistical analysis
@lru_cache(maxsize=2048) # speed up file reading by caching the results
def get_values(filepath, params=("total_cycles", "sched_stalls", "occupancy")):
    params_dict = {
        "total_cycles": {"name": "gpu_tot_sim_cycle", "lambda": lambda line: float(line[2])},
        "sched_stalls": {"name": "STALLING_VALUES", "lambda": lambda line: int(line[1])},
        "occupancy": {"name": "gpu_tot_occupancy", "lambda": lambda line: float(line[2][:-1])},
    }

    res = [-1 for _ in range(len(params))]
    with open(filepath, "r") as fin:
        i = 0
        for line in fin:
            i += 1
            try:
                line_split = line.strip().split()
                for k, param in enumerate(params):
                    if params_dict[param]["name"] in line:
                        res[k] = params_dict[param]["lambda"](line_split)
            except Exception as e:
                print(f"Error in line {i} in file {filepath}")
                print(line)
                raise e
    return res

@lru_cache(maxsize=2048) # speed up file reading by caching the results
def get_total_cycles(filepath):
    return get_values(filepath)[0]

@lru_cache(maxsize=2048) # speed up file reading by caching the results
def get_scheduler_stalls(filepath):
    return get_values(filepath)[1]

@lru_cache(maxsize=2048) # speed up file reading by caching the results
def get_occupancy(filepath):
    return get_values(filepath)[2]

def write_csv_header(csv_writer, all_folders, param_names=(lambda x: x, lambda x: f"{x}_sched"), name_rule=(lambda x:x)):
    headers = ["Benchmark"] + [f"{name(name_rule(foldername))}" for test_set in all_folders for foldername in test_set[1:] for name in param_names]
    csv_writer.writerow(headers)

def get_speedup_numbers(csv_writer, all_folders, benchmarks, directory, params=("total_cycles", "sched_stalls", "occupancy"), 
                        geo=False, geo_only=False):
    param_funcs = {
        "total_cycles": {"func": get_total_cycles, "parse": lambda v, base: (base - v) / base + 1 if base > 0 else 0},
        "sched_stalls": {"func": get_scheduler_stalls, "parse": lambda v, base: (base - v) / base + 1 if base > 0 else 0},
        "occupancy": {"func": get_occupancy, "parse": lambda v, _: v if v > 0 else 0}
    }
    
    geo = geo or geo_only
    all_data = {filename: [] for filename in benchmarks}
    geo_means = [1 for _ in range(sum(len(testset) - 1 for testset in all_folders) * len(params))]
    geo_counts = [0 for _ in range(sum(len(testset) - 1 for testset in all_folders) * len(params))]
    
    print(f"Size of all_folders: {len(all_folders)} [ {[len(x) for x in all_folders]} ]")
    print(f"Size of benchmarks: {len(benchmarks)}")
    print(f"Size of params: {len(params)}")
    print(f"Size of geo_means: {len(geo_means)}")
    
    # Pre-calculate all required data to avoid repetition file readings
    column_index = -1 # start one before 0
    for param in params:
        for testset in all_folders:
            for foldername in testset[1:]:
                column_index += 1
                for filename in benchmarks:
                    base_value = param_funcs[param]["func"](directory / testset[0] / filename)
                    import_value = param_funcs[param]["func"](directory / foldername / filename)
                    all_data[filename].append(param_funcs[param]["parse"](import_value, base_value))
                    print(f"[Column {column_index}] -- {foldername} / {filename} : {param} = {import_value} by {base_value}")
                    if import_value == -1:
                        print(f"\033[31mError: {directory}/{foldername}/{filename} does not have {param} value\033[0m")
                    if all_data[filename][-1] > 0:
                        if geo:
                            geo_means[column_index] *= all_data[filename][-1]
                            geo_counts[column_index] += 1
                    
    # Write the calculated speedup data
    if not geo_only:
        for filename, data in all_data.items():
            csv_writer.writerow([filename] + data)

    if geo:
        geo_line = ["geomean"] + ([geo_means[i] ** (1 / geo_counts[i]) for i in range(len(geo_means))])
        csv_writer.writerow(geo_line)

def get_load_distribution(benchmark,configs,directory, output_file):
    PCs = [976,1440,1232,992,1472,1248]
    for foldername in configs:
        for filename in benchmark:
            PC_vals_temp = []
            # add a list for each PC
            for i in range(len(PCs)):
                PC_vals_temp.append([])
            filepath = directory / foldername / filename
            fin=open(filepath,"r")
            collect_numbers = False
            for line in fin:
                line = line.strip()
                line1 =  line.split(' ')
                if("kernel id" in line):
                    if(int(line1[-1])==3):
                        collect_numbers = True
                    else:
                        collect_numbers = False
                
                if "INST_ISSUE_CYCLE" in line and collect_numbers == True:
                    PC = int(line1[1])
                    num_cycle = int(line1[3])
                    if PC in PCs:
                        index = PCs.index(PC)
                        PC_vals_temp[index].append(num_cycle)
            output_name = filename.split("-")[-1].split(".")[0]
            print(f"Writing to {output_file} for Fig 3")
            with open(output_file, mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["#"] + PCs)
                for k in range(len(PC_vals_temp[0])):
                    csv_writer.writerow([k] + [PC_vals_temp[i][k] for i in range(len(PCs))])

def get_all_benchmarks():
    return [
        "slurm-backprop.out", "slurm-bfs_rodinia.out", "slurm-b+tree_rodinia.out", "slurm-dwt2d_rodinia.out",
        "slurm-gaussian.out", "slurm-lavaMD_rodinia.out", "slurm-lud.out", "slurm-myocyte.out", "slurm-nn.out",
        "slurm-particlefinder_float.out", "slurm-srad_v1_rodinia.out", "slurm-beamformer.out",
        "slurm-convolution_reduced.out", "slurm-dct.out", "slurm-des_pagoda.out", "slurm-mandelbort.out",
        "slurm-matrixMul_pagoda.out", "slurm-multiwork.out", "slurm-fw.out", "slurm-sssp_pannotia.out",
        "slurm-ispass-BFS.out", "slurm-LPS.out", "slurm-LIB.out", "slurm-RAY.out", "slurm-STO.out", "slurm-CN.out",
        "slurm-GRU.out", "slurm-LSTM.out"
    ]
# Main function definition
def fig_3(directory, output_file="fig_3.csv"):
    benchmark = ["slurm-sssp_pannotia.out"]
    configs = ["SASS_load_latency"]
    get_load_distribution(benchmark,configs,directory, output_file)

def fig_13(directory, output_file="fig_13.csv"):
    configs = [["IN_4", "IBOOO_8"]]
    benchmarks = get_all_benchmarks()

    with open(output_file, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        write_csv_header(csv_writer, configs, param_names=(lambda x: x, lambda x: f"{x}_sched", lambda x: f"{x}_occupancy"))
        get_speedup_numbers(csv_writer, configs, benchmarks, directory, params=("total_cycles", "sched_stalls", "occupancy"), geo=True)

def fig_14(directory, output_file="fig_14.csv"):
    configs = [["IN_4", "GP_4", "GP_8", "GP_16", "GP_32"]]
    benchmarks = get_all_benchmarks()

    with open(output_file, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        write_csv_header(csv_writer, configs, param_names=(lambda x: x, ), name_rule=(lambda x: x.split("_")[-1]))
        get_speedup_numbers(csv_writer, configs, benchmarks, directory, params=("total_cycles", ), geo=True)

def fig_15(directory, output_file="fig_15.csv"):
    configs_2060s = ["IN_4", "IBOOO_4", "IBOOO_8", "IBOOO_16", "IBOOO_32",]
    configs_2070 = ["IN_4_RTX3070","IBOOO_4_RTX3070", "IBOOO_8_RTX3070", "IBOOO_16_RTX3070","IBOOO_32_RTX3070",]
    benchmarks = get_all_benchmarks()

    with open(output_file, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        configs = [configs_2060s, configs_2070]
        write_csv_header(csv_writer, configs, param_names=(lambda x: x, ))
        get_speedup_numbers(csv_writer, configs, benchmarks, directory, params=("total_cycles", ), geo=True)

def fig_16(directory, output_file="fig_16.csv"):
    configs_GTO = ["IN_4", "IBOOO_8"]
    configs_LRR = ["IN_4_LRR", "IBOOO_8_LRR"]
    configs_SRR = ["IN_4_SRR", "IBOOO_8_SRR"]
    benchmarks = get_all_benchmarks()
    
    with open(output_file, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        configs = [configs_GTO, configs_LRR, configs_SRR]
        names = {"IBOOO_8": "GTO", "IBOOO_8_LRR": "LRR", "IBOOO_8_SRR": "SRR"}
        write_csv_header(csv_writer, configs, param_names=(lambda x: x, ), name_rule=(lambda x: names[x]))
        get_speedup_numbers(csv_writer, configs, benchmarks, directory, params=("total_cycles", ), geo=True)

def fig_17(directory, output_file="fig_17.csv"):
    configs_ghost = ["IN_4", "IBOOO_8"]
    configs_loog = ["IN_4", "LOOG_OoO"]
    benchmarks = get_all_benchmarks()
    
    with open(output_file, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        configs = [configs_ghost, configs_loog]
        write_csv_header(csv_writer, configs, param_names=(lambda x: x, ))
        get_speedup_numbers(csv_writer, configs, benchmarks, directory, params=("total_cycles", ), geo=True)

def fig_19(directory, output_file="fig_19.csv"):
    configs_ghost = ["IN_4", "IBOOO_8"]
    configs_loog = ["IN_4", "LOOG_OoO"]
    benchmarks = get_all_benchmarks()
    
    with open(output_file, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        configs = [configs_ghost, configs_loog]
        write_csv_header(csv_writer, configs, param_names=(lambda x: x, ))
        get_speedup_numbers(csv_writer, configs, benchmarks, directory, params=("total_cycles", ), geo=True)


def example(output_file="example.csv"):
    all_folders = [["IN_4", "IBOOO_4", "IBOOO_8", "IBOOO_16", "IBOOO_32", "GP_4", "GP_8", "GP_16", "GP_32"]]
    benchmarks = get_all_benchmarks()

    with open(output_file, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        write_csv_header(csv_writer, all_folders, param_names=(lambda x: x, lambda x: f"{x}_sched"))
        get_speedup_numbers(csv_writer, all_folders, benchmarks, directory, params=("total_cycles", "sched_stalls"))

if __name__ == "__main__":
    directory = Path(__file__).parent
    if (str(directory).split("/")[-1] == "ghost_scripts"):
        directory = directory.parent
        
    print("Current directory: ", directory)
    outfile_folder = directory / "results"
    outfile_folder.mkdir(exist_ok=True)

    # example(output_file=outfile_folder / "cycle_count.csv")
    fig_table = {
        "fig_3": fig_3,
        "fig_13": fig_13,
        "fig_14": fig_14,
        "fig_15": fig_15,
        "fig_16": fig_16,
        "fig_17": fig_17,
        "fig_19": fig_19
    }
    for k, v in fig_table.items():
        print(f"Running {k} to {outfile_folder / f'{k}.csv'}")
        v(directory / "collect_results_artifact", output_file=outfile_folder / f"{k}.csv")
        print("\n")
        
    