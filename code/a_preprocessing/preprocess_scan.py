import os
import subprocess
from pathlib import Path

def kick_off_preprocessing(sub,
						   session,
						   task,
						   run,
						   anat_path,
						   func_path,
						   base_dir,
						   process_round):

	process_script_name = f'preprocessing_{process_round}.sh'

	if not os.path.exists(f'{base_dir}/derivatives/sub-{sub}/ses-{session}/{process_round}'):
		os.makedirs(f'{base_dir}/derivatives/sub-{sub}/ses-{session}/{process_round}')

	base_dir_process_round = f'{base_dir}/derivatives/sub-{sub}/ses-{session}/{process_round}'
	results_dir = f'{base_dir_process_round}/{sub}.{session}.{task}.{run}.results'
	slurm_file = f'{base_dir_process_round}/{process_round}_{sub}_{session}_{task}_{run}_submit.sh'
	proc_file  = f'{base_dir_process_round}/proc.{sub}_{session}_{task}_{run}'
	slurm_out = f'{base_dir_process_round}/slurm_out_{sub}_{session}_{task}_{run}.sh'


	try:
		# rm old results dir, old proc file (generated  by afni), & old slurm file
		os.rmdir(results_dir)
		os.remove(proc_file)
		os.remove(slurm_file)
	except:
		# if this is our  first  time running, may not  have the above files/folder
		#  so running will throw an error we want to ignore
		pass

	# make new  slurmfile
	subprocess.call(['touch', slurm_out])
	with open(slurm_file, 'w') as f:
		f.write(f"""#!/bin/bash
#SBATCH --partition=broadwl
#SBATCH --time=04:00:00
#SBATCH --account=pi-mdrosenberg
#SBATCH --output={slurm_out}
#SBATCH --ntasks=1 --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --job-name=AVA
#SBATCH --mem-per-cpu=9000
bash ./afni_proc_scripts/{process_script_name} {sub} {session} {task} {run} {anat_path} {func_path} {base_dir}""")

	cmd = f'sbatch < {slurm_file}'
	status, jobnum_line = subprocess.getstatusoutput(cmd)

	jobnum = jobnum_line.replace('Submitted batch job ', '')
	return jobnum


def preprocess_scan(sub, session, task, run, start_at, base_dir='/project/mdrosenberg/ava/ava_pipeline/data'):
	jobnum = None
	completed_job_num = 7570330

	# define directories
	data_dir= f'{base_dir}/sub-{sub}'
	img_name =  task

	# PREPROCESSING
	anat_img = f'{data_dir}/ses-{session}/anat/sub-{sub}_ses-{session}_acq-MPRAGE_run-01_T1w.nii.gz'
	func_img = f'{data_dir}/ses-{session}/func/sub-{sub}_ses-{session}_task-{task}_run-{run}_bold.nii.gz'
	if os.path.exists(anat_img) and os.path.exists(func_img):
		if start_at=='step1_getmotion':
			jobnum = jobnum or completed_job_num
			jobnum = kick_off_preprocessing(sub,
											session,
											task,
											run,
											anat_img,
											func_img,
											base_dir,
											process_round='step1_getmotion')

			print(f'kick off step1_getmotion preproc, sub: {sub} session: {session} task: {task} run: {run} jobid: {jobnum}')

		if start_at=='step1_getmotion_mot_censor':
			jobnum = jobnum or completed_job_num
			jobnum = kick_off_preprocessing(sub,
											session,
											task,
											run,
											anat_img,
											func_img,
											base_dir,
											process_round='step1_getmotion_mot_censor')

			print(f'kick off step1_getmotion with motion censor preproc, sub: {sub} session: {session} task: {task} run: {run} jobid: {jobnum}')


		if start_at=='step2_24motparam':
			jobnum = jobnum or completed_job_num
			jobnum = kick_off_preprocessing(sub,
											session,
											task,
											run,
											anat_img,
											func_img,
											base_dir,
											process_round='step2_24motparam')

			print(f'kick off step2_24motparam preproc, sub: {sub} session: {session} task: {task} run: {run} jobid: {jobnum}')


		if start_at=='step2_24motparam_mot_censor':
			jobnum = jobnum or completed_job_num
			jobnum = kick_off_preprocessing(sub,
											session,
											task,
											run,
											anat_img,
											func_img,
											base_dir,
											process_round='step2_24motparam_mot_censor')

			print(f'kick off step2_24motparam with motion censor preproc, sub: {sub} session: {session} task: {task} run: {run} jobid: {jobnum}')


		if start_at=='step2_24motparam_mot_censor_test':
			jobnum = jobnum or completed_job_num
			jobnum = kick_off_preprocessing(sub,
											session,
											task,
											run,
											anat_img,
											func_img,
											base_dir,
											process_round='step2_24motparam_mot_censor_test')

			print(f'kick off step2_24motparam with motion censor test preproc, sub: {sub} session: {session} task: {task} run: {run} jobid: {jobnum}')
