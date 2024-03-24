#!/bin/bash
#SBATCH --job-name=sssp_pannotia     # create a short name for your job
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=16G         # memory per cpu-core (4G per cpu-core is default)
#SBATCH --time=23:00:00          # total run time limit (HH:MM:SS)
#SBATCH --output=slurm-%x.out
#SBATCH --error=slurm-%x.err

export SINGULARITYENV_LD_LIBRARY_PATH=/mylibs
nohup singularity exec -B $LOOG_LIBCUDA:/mylibs $SINGULARITY_IMG bash sssp_pannotia.sh
