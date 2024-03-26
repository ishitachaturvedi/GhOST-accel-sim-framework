# set and test our main path, this needs to be done everytime
export ACCEL_SIM_DIR=`pwd`
# test the path [optional]
[ ! -d "$ACCEL_SIM_DIR/ghost_scripts" ] && echo "Error: Directory $ACCEL_SIM_DIR/ghost_scripts does not exist" > /dev/stderr

# load LOOG simulator files (untar at background)
tar -xzf gpu-simulator-LOOG.tar.gz &

# load SASS traces [zenode link]
tar -xzf GhOST_SASS_traces.tar.gz & 

# load area calculation [zenode link]
tar -xzf GhOST-area-calculation.tar.gz &

# load image file [zenode link]

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

