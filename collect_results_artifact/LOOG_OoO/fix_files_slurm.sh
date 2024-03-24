#!/bin/bash

# Define the list of files
FILES="backprop.slurm bfs_rodinia.slurm b+tree_rodinia.slurm dwt2d_rodinia.slurm gaussian.slurm lavaMD_rodinia.slurm lud.slurm myocyte.slurm nn.slurm particlefinder_float.slurm srad_v1_rodinia.slurm beamformer.slurm dct.slurm des_pagoda.slurm mandelbort.slurm matrixMul_pagoda.slurm multiwork.slurm fw.slurm sssp_pannotia.slurm ispass-BFS.slurm LPS.slurm LIB.slurm RAY.slurm STO.slurm CN.slurm GRU.slurm LSTM.slurm convolution_reduced.slurm"

# Loop through each file
for file in $FILES; do
    # Make replacements in the SLURM file
    #sed -i.backup "s|/scratch/gpfs/ishitac/gpgpusim-codes/accel-sim-framework|\$ACCEL_SIM_DIR|g" "$file"
    #sed -i.backup "s|/home/ishitac/tigress/gpu-accel-sim-docker.img|\$SINGULARITY_IMG|g" "$file"
    #sed -i.backup '/#SBATCH --mail-type=fail/d' "$file"
    #sed -i.backup '/#SBATCH --mail-user=ishitac@princeton.edu/d' "$file"
    sed -i.backup "s|\$ACCEL_SIM_DIR/gpu-simulator/gpgpu-sim/lib/gcc-7.5.0/cuda-11060/release|\$LOOG_LIBCUDA|g" "$file"
    # Remove backup files
    rm "$file.backup"
done

echo "Changes made successfully."
