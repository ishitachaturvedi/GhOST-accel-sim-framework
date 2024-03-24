#!/bin/bash

FILES=("sssp_pannotia.slurm")

# for file in $FILES; do
#     echo "$(basename "$file")"
# done

for f in $FILES; do
   echo "starting " $f
   sbatch $f
done
