#!/bin/bash

FILES=" backprop.slurm
        bfs_rodinia.slurm
        b+tree_rodinia.slurm
        dwt2d_rodinia.slurm
        gaussian.slurm
        lavaMD_rodinia.slurm
        lud.slurm
        myocyte.slurm
        nn.slurm
        particlefinder_float.slurm
        srad_v1_rodinia.slurm
        beamformer.slurm
        dct.slurm
        des_pagoda.slurm
        mandelbort.slurm
        matrixMul_pagoda.slurm
        fw.slurm
        sssp_pannotia.slurm
        ispass-BFS.slurm
        LPS.slurm
        RAY.slurm
        STO.slurm
        CN.slurm
        GRU.slurm
        LSTM.slurm
	convolution_reduced.slurm
        "

# for file in $FILES; do
#     echo "$(basename "$file")"
# done

for f in $FILES; do
   echo "starting " $f
   sbatch $f
done
