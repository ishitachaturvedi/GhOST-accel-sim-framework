#!/bin/bash

# Get the current script directory reliably
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR/.." || exit
echo "Current working dir is $(pwd)"

# attemp to set $ACCEL_SIM_DIR if possible
export ACCEL_SIM_DIR=${ACCEL_SIM_DIR:-$(pwd)}
# test environment
[ ! -d "$ACCEL_SIM_DIR/ghost_scripts" ] && echo "Error: Directory $ACCEL_SIM_DIR/ghost_scripts does not exist" > /dev/stderr

# Check directories and files exist
[[ ! -d "$ACCEL_SIM_DIR" ]] && echo "ERROR: \$ACCEL_SIM_DIR not found" >&2 && exit 1

echo "Executing run_test.sh"
bash $SCRIPT_DIR/run_test.sh

echo "Executing run_area.sh"
bash $SCRIPT_DIR/run_area.sh
