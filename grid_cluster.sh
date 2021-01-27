#!/bin/bash
#SBATCH --array 0-1000
#SBATCH -p cubric-default
#SBATCH --job-nam=gridww
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 1
#SBATCH -o logs/wwi_%j.out
#SBATCH -e logs/wwi_%j.err
python grid_ww_iter.py gridvals/
