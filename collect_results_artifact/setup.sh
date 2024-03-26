# get git folder
wget "https://zenodo.org/records/10847246/files/GhOST-accel-sim-framework-dev.zip?download=1&preview=1" -O GhOST-accel-sim-framework.tar.gz
tar -xzf GhOST-accel-sim-framework.tar.gz
cd GhOST-accel-sim-framework

# set and test our main path, this needs to be done everytime
export ACCEL_SIM_DIR=`pwd`
# test the path [optional]
[ ! -d "$ACCEL_SIM_DIR/ghost_scripts" ] && echo "Error: Directory $ACCEL_SIM_DIR/ghost_scripts does not exist" > /dev/stderr

# load LOOG simulator files (untar at background)
tar -xzf gpu-simulator-LOOG.tar.gz &

# load SASS traces [zenode link]
wget "https://zenodo.org/records/10847246/files/GhOST_SASS_traces.tar.gz?download=1&preview=1" -O GhOST_SASS_traces.tar.gz
tar -xzf GhOST_SASS_traces.tar.gz & 

# load area calculation [zenode link]
wget "https://zenodo.org/records/10847246/files/GhOST-area-calculation.tar.gz?download=1&preview=1" -O GhOST-area-calculation.tar.gz
tar -xzf GhOST-area-calculation.tar.gz &

# load image file [zenode link]
wget "https://zenodo.org/records/10847246/files/gpu-accel-sim-docker.img?download=1&preview=1" -O gpu-accel-sim-docker.img &

# Wait for all background jobs to finish
echo "Wait for all background jobs to finish ..." >&2
wait

# TOTAL FOLDER SIZE AT THIS MOMENT: about 46GB

### for build
echo "Running build script" >&2
bash ghost_scripts/run_build.sh

## have a minimal test for the setup
echo "Running minimal test" >&2
bash ghost_scripts/run_minimal_test.sh

