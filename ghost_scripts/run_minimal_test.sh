#!/bin/bash

# Get the current script directory reliably
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR/.." || exit
echo "Current working dir is $(pwd)"

# test environment
[ ! -d "$ACCEL_SIM_DIR/ghost_scripts" ] && echo "Error: Directory $ACCEL_SIM_DIR/ghost_scripts does not exist" > /dev/stderr

export SASS_dir=${SASS_dir:-$ACCEL_SIM_DIR/GhOST_SASS_traces}
export SINGULARITY_IMG=${SINGULARITY_IMG:-$ACCEL_SIM_DIR/gpu-accel-sim-docker.img}

# Check if the following env variables are set
for var in ACCEL_SIM_DIR SASS_dir SINGULARITY_IMG; do
    if [ -z "${!var}" ]; then  # Using indirect parameter expansion to check variables dynamically
        echo "ERROR: \$$var not set" >&2
        exit 1
    fi
done

# Check directories and files exist
[[ ! -d "$ACCEL_SIM_DIR" ]] && echo "ERROR: \$ACCEL_SIM_DIR not found" >&2 && exit 1
[[ ! -d "$SASS_dir" ]] && echo "ERROR: \$SASS_dir not found" >&2 && exit 1
[[ ! -f "$SINGULARITY_IMG" ]] && echo "ERROR: \$SINGULARITY_IMG not found" >&2 && exit 1

echo "Found \$ACCEL_SIM_DIR = $ACCEL_SIM_DIR "
echo "Found \$SASS_dir = $SASS_dir "
echo "Found \$SINGULARITY_IMG = $SINGULARITY_IMG "

run_tests() {
    local build_config=$1
    shift
    local configs=("$@")

    export BUILD_CONFIG=$build_config

    for config in "${configs[@]}"; do
        echo "Start all runs at ./collect_results_artifact/$config"
        # Ensure the directory exists before attempting to enter and execute
        if [ -d "collect_results_artifact/$config" ]; then
            if [ "$DRY_RUN" == "true" ]; then
                echo "DRY RUN: (cd collect_results_artifact/$config && sbatch LSTM.slurm)"
            else
                (cd "collect_results_artifact/$config" && sbatch LSTM.slurm)
            fi
        else
            echo "Directory collect_results_artifact/$config does not exist" >&2
        fi
    done
    sleep 5s
}

# In order tests
in_order_configs=("IN_4" "IN_4_LRR" "IN_4_RTX3070" "IN_4_SRR")
run_tests "-in-order" "${in_order_configs[@]}"

# OoO tests
ooo_configs=("IBOOO_16" "IBOOO_32_RTX3070" "IBOOO_64_BP_RMI_RR" "IBOOO_8_RTX3070" 
            "IBOOO_16_RTX3070" "IBOOO_4" "IBOOO_8" "IBOOO_8_SRR" 
            "IBOOO_32" "IBOOO_4_RTX3070" "IBOOO_8_LRR")
run_tests "-ooo" "${ooo_configs[@]}"

# Latency tests
# latency_configs=("SASS_load_latency")
# run_tests "-ldlat" "${latency_configs[@]}"

# GP tests
gp_configs=("GP_16" "GP_32" "GP_4" "GP_8")
run_tests "-gp" "${gp_configs[@]}"

# LOOG tests
export LOOG_DIR=$ACCEL_SIM_DIR/gpu-simulator-LOOG/bin/release
export LOOG_LIBCUDA=$ACCEL_SIM_DIR/gpu-simulator-LOOG/lib/release
if [ -d "$LOOG_DIR" ] && [ -d "$LOOG_LIBCUDA" ]; then
    loog_configs=("LOOG_OoO")
    run_tests "" "${loog_configs[@]}"
else
    echo "LOOG directories not found, skipping LOOG tests" >&2
fi