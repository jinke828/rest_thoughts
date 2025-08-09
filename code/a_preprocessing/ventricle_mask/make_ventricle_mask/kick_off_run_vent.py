import os
import subprocess


def kick_off_run_vent():
    slurm_file = 'slurm_file_vent_mask_run.sh'
    slurm_out = 'slurm_out_vent_mask_run.out'

    base_dir = '/project2/mdrosenberg/ava/ava_pipeline/data'
    sub = 'sub-pilot001'
    anat_path = f'{base_dir}/{sub}/anat/{sub}_acq-MPRAGE_run-01_T1w.nii.gz'
    func_path = f'{base_dir}/{sub}/func/{sub}_task-aNT_run-01_bold.nii.gz'

    # make new  slurmfile
    subprocess.call(['touch', slurm_out])
    with open(slurm_file, 'w') as f:
        f.write(f"""#!/bin/bash
#SBATCH --partition=broadwl
#SBATCH --exclusive -N1 -n1
#SBATCH --time=04:00:00
#SBATCH --output={slurm_out}
bash preprocessing_vent.sh pilot001 01 aNT 01 {anat_path} {func_path} {base_dir}
""")

    cmd = f'sbatch < {slurm_file}'
    status, jobnum_line = subprocess.getstatusoutput(cmd)

    jobnum = jobnum_line.replace('Submitted batch job ', '')
    return jobnum


kick_off_run_vent()
