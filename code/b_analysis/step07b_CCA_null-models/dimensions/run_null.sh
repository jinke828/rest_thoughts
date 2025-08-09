#!/bin/bash

#SBATCH --job-name=CCA_d
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5G

module reset
module load miniconda
module load python
source activate aigonauts
python run_null.py --myvar=$1