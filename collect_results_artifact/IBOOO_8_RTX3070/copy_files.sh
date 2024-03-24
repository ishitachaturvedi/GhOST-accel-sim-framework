#!/bin/bash

# Define the list of files
FILES="backprop.sh bfs_rodinia.sh b+tree_rodinia.sh dwt2d_rodinia.sh gaussian.slurm lavaMD_rodinia.slurm lud.slurm myocyte.slurm nn.slurm particlefinder_float.slurm srad_v1_rodinia.slurm beamformer.slurm dct.slurm des_pagoda.slurm mandelbort.slurm matrixMul_pagoda.slurm multiwork.slurm fw.slurm sssp_pannotia.slurm ispass-BFS.slurm LPS.slurm LIB.slurm RAY.slurm STO.slurm CN.slurm GRU.slurm LSTM.slurm convolution_reduced.slurm"

# Loop through each file
for file in $FILES; do
    # Copy the file from IN_4 directory to the current directory
    cp "../IN_4/$file" .
done
