#!/bin/bash

# Get the current script directory reliably
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR/.." || exit
echo "Current working dir is $(pwd)"

# attemp to set $ACCEL_SIM_DIR if possible
export ACCEL_SIM_DIR=${ACCEL_SIM_DIR:-$(pwd)}
# test environment
[ ! -d "$ACCEL_SIM_DIR/ghost_scripts" ] && echo "Error: Directory $ACCEL_SIM_DIR/ghost_scripts does not exist" > /dev/stderr

export CUDA_INSTALL_PATH=/usr/local/cuda-11
export PATH=$CUDA_INSTALL_PATH/bin:$CUDA_INSTALL_PATH/targets/x86_64-linux/lib:$PATH
export SASS_dir=${SASS_dir:-$ACCEL_SIM_DIR/GhOST_SASS_traces}
export SINGULARITY_IMG=${SINGULARITY_IMG:-$ACCEL_SIM_DIR/gpu-accel-sim-docker.img}
export area_base=${area_base:-$ACCEL_SIM_DIR/GhOST-area-calculation}

# Check if the following env variables are set
for var in ACCEL_SIM_DIR SASS_dir SINGULARITY_IMG area_base SYNOPSYS_PATH SYNOPSYS_ICC2_PATH; do
    if [ -z "${!var}" ]; then  # Using indirect parameter expansion to check variables dynamically
        echo "ERROR: \$$var not set" >&2
        exit 1
    fi
done

# Check directories and files exist
[[ ! -d "$ACCEL_SIM_DIR" ]] && echo "ERROR: \$ACCEL_SIM_DIR not found" >&2 && exit 1
[[ ! -d "$SASS_dir" ]] && echo "ERROR: \$SASS_dir not found" >&2 && exit 1
[[ ! -f "$SINGULARITY_IMG" ]] && echo "ERROR: \$SINGULARITY_IMG not found" >&2 && exit 1
[[ ! -d "$area_base" ]] && echo "ERROR: \$area_base not found" >&2 && exit 1
[[ ! -d "$SYNOPSYS_PATH" ]] && echo "ERROR: \$SYNOPSYS_PATH not found" >&2 && exit 1
[[ ! -d "$SYNOPSYS_ICC2_PATH" ]] && echo "ERROR: \$SYNOPSYS_ICC2_PATH not found" >&2 && exit 1

echo "Found \$ACCEL_SIM_DIR = $ACCEL_SIM_DIR "
echo "Found \$SASS_dir = $SASS_dir "
echo "Found \$SINGULARITY_IMG = $SINGULARITY_IMG "
echo "Found \$area_base = $area_base "
echo "Found \$SYNOPSYS_PATH = $SYNOPSYS_PATH "
echo "Found \$SYNOPSYS_ICC2_PATH = $SYNOPSYS_ICC2_PATH "

# Area and Power model
(cd $area_base && bash collect_area_stats.sh)