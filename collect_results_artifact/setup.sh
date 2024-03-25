# get git folder
git clone --recurse-submodules https://github.com/ishitachaturvedi/GhOST-accel-sim-framework/
cd GhOST-accel-sim-framework

# set and test our main path, this needs to be done everytime
export ACCEL_SIM_DIR=`pwd`
# test the path [optional]
[ ! -d "$ACCEL_SIM_DIR/ghost_scripts" ] && echo "Error: Directory $ACCEL_SIM_DIR/ghost_scripts does not exist" > /dev/stderr

# load LOOG simulator files (untar at background)
tar -xzf gpu-simulator-LOOG.tar.gz &

# load SASS traces [zenode link]
wget "http://dl.dropboxusercontent.com/scl/fi/mojmdrllvv04ybbdnjp8n/GhOST_SASS_traces.tar.gz?rlkey=ij27ex7mrjnhybo53oossetv6&dl=0" -O GhOST_SASS_traces.tar.gz
tar -xzf GhOST_SASS_traces.tar.gz & 

# load area calculation [zenode link]
wget "http://dl.dropboxusercontent.com/scl/fi/hbrthlutldyvyge2u205v/GhOST-area-calculation.tar.gz?rlkey=e6kli4ojfeqkeuytysy6ybc0f&dl=0" -O GhOST-area-calculation.tar.gz
tar -xzf GhOST-area-calculation.tar.gz &

# load image file [zenode link]
wget "http://dl.dropboxusercontent.com/scl/fi/w39fuxejxja1y8f8ciog8/gpu-accel-sim-docker.img?rlkey=zqbgaua0xdiq7tc4zr2lk42c1&dl=0" -O gpu-accel-sim-docker.img &

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

