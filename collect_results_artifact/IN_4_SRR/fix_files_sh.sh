#!/bin/bash

# Define the list of files
FILES="backprop.sh bfs_rodinia.sh b+tree_rodinia.sh dwt2d_rodinia.sh gaussian.sh lavaMD_rodinia.sh lud.sh myocyte.sh nn.sh particlefinder_float.sh srad_v1_rodinia.sh beamformer.sh dct.sh des_pagoda.sh mandelbort.sh matrixMul_pagoda.sh multiwork.sh fw.sh sssp_pannotia.sh ispass-BFS.sh LPS.sh LIB.sh RAY.sh STO.sh CN.sh GRU.sh LSTM.sh convolution_reduced.sh"

# Loop through each file
for file in $FILES; do
    # Make replacements in the sh file
    sed -i.backup "s|accel-sim.out|accel-sim-in-order.out|g" "$file"
    # sed -i.backup "s|\$ACCEL_SIM_DIR/hw_run_back|\$SASS_dir|g" "$file"
    # sed -i.backup "s|\$ACCEL_SIM_DIR/pagoda_traces|\$SASS_dir|g" "$file"
    # sed -i.backup "s|\$ACCEL_SIM_DIR/altis|\$SASS_dir|g" "$file"
    # sed -i.backup "s|\$SASS_dir/ISCA-24-Bmrks|\$SASS_dir|g" "$file"
    # sed -i.backup "s|/scratch/gpfs/ishitac/gpgpusim-codes/accel-sim-framework/hw_run/traces/device-0/11.5|\$SASS_dir|g" "$file"
    # sed -i.backup "s|/scratch/gpfs/ishitac/gpgpusim-codes/accel-sim-framework|\$ACCEL_SIM_DIR|g" "$file"
    # Remove backup files
    rm "$file.backup"
done

echo "Changes made successfully."
