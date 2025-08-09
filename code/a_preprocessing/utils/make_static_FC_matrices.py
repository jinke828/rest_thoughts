import sys
import os

def make_static_FC_matrices(sub, session, data_type, run, sub_results_dir):
	sub_id_only = sub.replace('sub-', '')

	# need to check if its ok not to use a mask
	# but it appears our code doesn't generate one
	# from docs
	# If no mask is input, then
    #                   the program will internally 'automask', based on
    #                   when non-uniformly-zero time series are.
    #                   If you want to neither put in a mask *nor* have the
    # automasking occur, see '-automask_off', below.
	# cmd = 'cd ' + sub_results_dir +' && \
	#    module load afni/19.0 && '+'3dNetCorr -prefix '+ sub_id_only +'_' + session + '_'  + data_type + '_' + run + '_LPI \
	#   -mask ' + sub_results_dir + 'full_mask.'+sub_id_only+'.'+session +'.' + data_type+'.' + run + '+tlrc \
	#   -inset '+ sub_results_dir + 'errts.'+sub_id_only+'.'+session+'.'+data_type+'.'+run+'.tproject+tlrc \
	#   -in_rois /project2/mdrosenberg/ava/ava_pipeline/code/preprocessing/shen_atlas/shen_3mm_3mm_3_75mm_268_parcellation_resampled_ava_master+tlrc\
	#   -fish_z \
	#   -ts_out \
	#   -push_thru_many_zeros'
	#
	#   if 'step1_polort' in sub_results_dir:
	# 	  cmd = 'cd ' + sub_results_dir +' && \
	# 	  module load afni/19.0 && '+'3dNetCorr -prefix '+ sub_id_only +'_' + session + '_'  + data_type + '_' + run + '_LPI \
	# 	  -inset '+ sub_results_dir + 'errts.'+sub_id_only+'.'+session+'.'+data_type+'.'+run+'.tproject+orig \
	# 	  -in_rois /project2/mdrosenberg/ava/ava_pipeline/code/preprocessing/shen_atlas/shen_3mm_3mm_3_75mm_268_parcellation_resampled_ava_master+tlrc\
	# 	  -fish_z \
	# 	  -ts_out \
	# 	  -push_thru_many_zeros'

	mask_line = f'-mask {sub_results_dir}/full_mask.{sub_id_only}.{session}.{data_type}.{run}+tlrc'
	inset_end = 'tlrc'

	if 'step1_polort' in sub_results_dir:
		# for polort step, use tproject+orig (dunno if this is ok)
		inset_end = 'orig'
		# and don't use a custom mask (since we don't make one)
		mask_line = ''

	cmd = f"""cd {sub_results_dir} &&
	   module load afni/19.0 && 3dNetCorr -prefix {sub_id_only}_{session}_{data_type}_{run}_LPI \
	  {mask_line} \
	  -inset {sub_results_dir}/errts.{sub_id_only}.{session}.{data_type}.{run}.tproject+{inset_end} \
	  -in_rois /project2/mdrosenberg/ava/ava_pipeline/code/preprocessing/shen_atlas/shen_3mm_3mm_3_75mm_268_parcellation_resampled_ava_master+tlrc \
	  -fish_z \
	  -ts_out \
	  -push_thru_many_zeros"""
	os.system(cmd)


print('sys.argv', sys.argv)
inputs = sys.argv[1:]
sub  = inputs[0]
session = inputs[1]
data_type  = inputs[2]
run = inputs[3]
sub_results_dir = inputs[4]

make_static_FC_matrices(sub, session, data_type, run, sub_results_dir)
