#!/bin/bash
#SBATCH --time=00:30:00  # Set a time limit of 30 minutes
#SBATCH --job-name=plot_job
#SBATCH --output=plot_job.out
#SBATCH --error=plot_job.err

# Get the current script directory reliably
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR/.." || exit
echo "Current working dir is $(pwd)"

# Set environment variables as needed
export ACCEL_SIM_DIR=${ACCEL_SIM_DIR:-$(pwd)}

# Check environment
if [ ! -d "$ACCEL_SIM_DIR/ghost_scripts" ]; then
    echo "Error: Directory $ACCEL_SIM_DIR/ghost_scripts does not exist" > /dev/stderr
    exit 1
fi

echo "WARNING: Please install required python3 lib (or pip here) if not installed"
echo "Execute: pip3 install --user -r $ACCEL_SIM_DIR/ghost_scripts/requirements.txt  # to install required python3 libs"

sleep 60s
# Execute plotting
set -x  # Echo commands
python $ACCEL_SIM_DIR/ghost_scripts/data_process.py
python $ACCEL_SIM_DIR/ghost_scripts/plot.py
