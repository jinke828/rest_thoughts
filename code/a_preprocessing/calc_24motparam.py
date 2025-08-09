import numpy as np
import sys
import os
import subprocess

def calculate_24motparam(subj, condition, first_pass_results_dir):
	calculated_24_motion_params_dir  = first_pass_results_dir + '/calculated_24_motion_params'
	if not os.path.exists(calculated_24_motion_params_dir):
		subprocess.call(['mkdir', calculated_24_motion_params_dir])

	outpath = calculated_24_motion_params_dir+ '/' + subj + '_' + condition + '_24_param.1D'
	motion_demean_file = first_pass_results_dir + '/motion_demean.1D'
	motion_deriv_file  = first_pass_results_dir + '/motion_deriv.1D'
	print(first_pass_results_dir)
	motion_demean_mat = np.genfromtxt(motion_demean_file)
	motion_deriv_mat = np.genfromtxt(motion_deriv_file)
	print(len(motion_demean_mat))
	motion_demean_mat_squared = np.square(motion_demean_mat)
	motion_deriv_mat_squared = np.square(motion_deriv_mat)
	print(len(motion_demean_mat_squared))

	mot_24_param =  np.concatenate((motion_demean_mat,
									motion_demean_mat_squared,
									motion_deriv_mat,
									motion_deriv_mat_squared), axis=1)

	np.savetxt(outpath, mot_24_param, delimiter='\t', fmt='%.6f')


input_args = sys.argv[1:]
subj = input_args[0]
condition = input_args[1]
first_pass_results_dir = input_args[2]
calculate_24motparam(subj, condition, first_pass_results_dir)
