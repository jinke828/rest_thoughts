#!/bin/bash
#SBATCH --partition=broadwl
#SBATCH --exclusive -N1 -n1
#SBATCH --time=04:00:00
#SBATCH --output=slurm_out_vent_mask_run.out
bash preprocessing_vent.sh pilot001 01 aNT 01 /project2/mdrosenberg/ava/data//sub-pilot001/anat/sub-pilot001_acq-MPRAGE_run-01_T1w.nii.gz /project2/mdrosenberg/ava/data//sub-pilot001/func/sub-pilot001_task-aNT_run-01_bold.nii.gz /project2/mdrosenberg/ava/data/
