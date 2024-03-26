#!/bin/bash

# Get the current script directory reliably
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR/.." || exit
echo "Current working dir is $(pwd)"

# attemp to set $ACCEL_SIM_DIR if possible
export ACCEL_SIM_DIR=${ACCEL_SIM_DIR:-$(pwd)}
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

declare -A all_job_ids  # Associative array to hold all job IDs categorized by build config
run_tests() {
    local build_config=$1
    shift
    local configs=("$@")
    local job_ids=()  # Array to store job IDs

    export BUILD_CONFIG=$build_config

    for config in "${configs[@]}"; do
        echo "Start all runs at ./collect_results_artifact/$config"
        # Ensure the directory exists before attempting to enter and execute
        if [ -d "collect_results_artifact/$config" ]; then
            if [ "$DRY_RUN" == "true" ]; then
                echo "DRY RUN: (cd collect_results_artifact/$config && bash run_all_scripts_ISCA.sh)"
            else
                sbatch_output=$(cd "collect_results_artifact/$config" && bash run_all_scripts_ISCA.sh)
                echo "$sbatch_output"
                # Extract the job ID and store it
                job_id=$(echo $sbatch_output | grep -oP 'Submitted batch job \K[0-9]+')
                job_ids+=($job_id)
            fi
        else
            echo "Directory collect_results_artifact/$config does not exist" >&2
        fi
    done
    # Store all job IDs for this batch
    all_job_ids[$build_config]="${job_ids[*]}"

    sleep 1s
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
latency_configs=("SASS_load_latency")
run_tests "-ldlat" "${latency_configs[@]}"

# GP tests
gp_configs=("GP_16" "GP_32" "GP_4" "GP_8")
run_tests "-gp" "${gp_configs[@]}"

# LOOG tests
export LOOG_DIR=$ACCEL_SIM_DIR/gpu-simulator-LOOG/bin/release
export LOOG_LIBCUDA=$ACCEL_SIM_DIR/gpu-simulator-LOOG/lib/release
if [ -d "$LOOG_DIR" ] && [ -d "$LOOG_LIBCUDA" ]; then
    loog_configs=("LOOG_OoO")
    run_tests "LOOG_OoO" "${loog_configs[@]}"
else
    echo "LOOG directories not found, skipping LOOG tests" >&2
fi

# At the end of the script, print all job IDs:
echo -e "\n\nAll tests submitted. Job IDs: "
SHORT_SCRIPT_DIR=$(basename $SCRIPT_DIR)
JOB_IDS_FILE="$SHORT_SCRIPT_DIR/test_job_ids.out"
rm -f "$JOB_IDS_FILE"  # Clear the file if it already exists

for config in "${!all_job_ids[@]}"; do
    echo "$config: ${all_job_ids[$config]}"
    echo -n "${all_job_ids[$config]} " >> "$JOB_IDS_FILE"
done


# Next steps
# Check if we are in a terminal
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    NO_COLOR='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    NO_COLOR=''
fi

# and prompt here to tell user, what happened.
echo -e "\nAll job IDs stored in $JOB_IDS_FILE"

barrier_job_output=$("$SCRIPT_DIR/run_barrier_job.sh" "$JOB_IDS_FILE")
BARRIER_JOB_ID=$(echo "$barrier_job_output" | grep -oP 'Barrier job submitted with ID: \K[0-9]+')
echo -e "\nA barrier job has been created to track the completeness of all jobs => Job ID: $BARRIER_JOB_ID${NO_COLOR}"
echo -e "You may use '${GREEN}squeue -j $BARRIER_JOB_ID${NO_COLOR}' to check the status of the barrier job."

# Provide hint for next steps.
echo -e "\n${YELLOW}After all jobs are completed, the script to plot the results will automatically start in the background.${NO_COLOR}"
echo -e "\nSubmitting the plot job to be executed after the barrier job completes..."
sbatch --dependency=afterany:$BARRIER_JOB_ID $SCRIPT_DIR/run_plot.slurm
# Run a plot script
# nohup bash -c "while squeue -j $BARRIER_JOB_ID | grep -q '$BARRIER_JOB_ID'; do sleep 10; done && bash '$SCRIPT_DIR/run_plot.sh'" &> /dev/null &

