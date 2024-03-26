#!/bin/bash
#SBATCH --time=00:30:00  # Set a time limit of 30 minutes
#SBATCH --job-name=min_plot_job
#SBATCH --output=min_plot_job.out
#SBATCH --error=min_plot_job.err

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
echo "Execute: pip3 install --user -r $ACCEL_SIM_DIR/ghost_scripts/requirements.txt  # to install required python3 lib (or pip here)"

sleep 60s
set -x
python $ACCEL_SIM_DIR/ghost_scripts/data_process.py -o min_ -b LSTM -d example
python $ACCEL_SIM_DIR/ghost_scripts/plot.py -p min_ -d example
