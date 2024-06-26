#!/bin/bash

# Get the current script directory reliably
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR/.." || exit
echo "Current working dir is $(pwd)"

# attemp to set $ACCEL_SIM_DIR if possible
export ACCEL_SIM_DIR=${ACCEL_SIM_DIR:-$(pwd)}
# test environment
[ ! -d "$ACCEL_SIM_DIR/ghost_scripts" ] && echo "Error: Directory $ACCEL_SIM_DIR/ghost_scripts does not exist" > /dev/stderr

### Parse data and plot performance diagrams
echo "WARNING: Please install required python3 lib (or pip here) if not installed"
echo "Execute: $   pip3 install --user -r $ACCEL_SIM_DIR/ghost_scripts/requirements.txt  # to install required python3 lib (or pip here)"

set -x
python $ACCEL_SIM_DIR/ghost_scripts/data_process.py
python $ACCEL_SIM_DIR/ghost_scripts/plot.py
