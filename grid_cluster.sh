#!/bin/bash
#SBATCH --array 0-1000
#SBATCH -p cubric-default
#SBATCH --job-nam=gridww
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 1
#SBATCH -o logs/wwi_%j.out
#SBATCH -e logs/wwi_%j.err
#python grid5_ww.py ${SLURM_ARRAY_TASK_ID} 1000
python ww2_grid_iter.py gridvalsf/
