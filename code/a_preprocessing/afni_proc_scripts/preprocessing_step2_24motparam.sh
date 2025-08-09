analysis () {

# set variables and data directories
sub=$1
session=$2
task=$3
run=$4
anat_path=$5
func_path=$6
base_dir=$7


mkdir -p ${base_dir}/derivatives/sub-${sub}/ses-${session}/step2_24motparam/
cd ${base_dir}/derivatives/sub-${sub}/ses-${session}/step2_24motparam/

module load python
python3 /project2/mdrosenberg/ava/ava_pipeline/code/preprocessing/calc_24motparam.py ${sub} ${task} ${base_dir}/derivatives/sub-${sub}/ses-${session}/step1_getmotion/${sub}.${session}.${task}.${run}.results

# run afni_proc.py to create a single subject processing script
# created by uber_subject.py: version 0.39 (March 21, 2016)
# creation date: Fri Apr  7 12:11:05 2017
afni_proc.py -subj_id ${sub}.${session}.${task}.${run}                                  \
	-script proc.${sub}_${session}_${task}_${run} -scr_overwrite                  \
	-blocks despike tshift align tlrc volreg mask regress  \
	-copy_anat ${anat_path}          \
	-dsets ${func_path}    \
	-tcat_remove_first_trs 3                              \
	-align_opts_aea -cost lpc+ZZ -giant_move              \
	-tlrc_base MNI_avg152T1+tlrc                          \
	-tlrc_NL_warp					                                \
	-volreg_align_to MIN_OUTLIER                          \
	-volreg_align_e2a                                     \
	-volreg_tlrc_warp                                     \
	-mask_segment_anat yes                                \
	-mask_segment_erode yes                               \
	-mask_import Tvent /project2/mdrosenberg/ava/ava_pipeline/code/preprocessing/ventricle_mask/mni_ventricle_template_ava_resample+tlrc \
	-mask_intersect Svent CSFe Tvent                      \
	-regress_ROI WMe Svent brain                          \
	-regress_apply_mot_types demean deriv                 \
  -regress_opts_3dD -num_stimts 12 \
		    -stim_file 1 ${base_dir}/derivatives/sub-${sub}/ses-${session}/step1_getmotion/${sub}.${session}.${task}.${run}.results/calculated_24_motion_params/${sub}_${task}_24_param.1D'[6]' -stim_base 1 \
		    -stim_file 2 ${base_dir}/derivatives/sub-${sub}/ses-${session}/step1_getmotion/${sub}.${session}.${task}.${run}.results/calculated_24_motion_params/${sub}_${task}_24_param.1D'[7]' -stim_base 2 \
		    -stim_file 3 ${base_dir}/derivatives/sub-${sub}/ses-${session}/step1_getmotion/${sub}.${session}.${task}.${run}.results/calculated_24_motion_params/${sub}_${task}_24_param.1D'[8]' -stim_base 3 \
		    -stim_file 4 ${base_dir}/derivatives/sub-${sub}/ses-${session}/step1_getmotion/${sub}.${session}.${task}.${run}.results/calculated_24_motion_params/${sub}_${task}_24_param.1D'[9]' -stim_base 4 \
		    -stim_file 5 ${base_dir}/derivatives/sub-${sub}/ses-${session}/step1_getmotion/${sub}.${session}.${task}.${run}.results/calculated_24_motion_params/${sub}_${task}_24_param.1D'[10]' -stim_base 5 \
		    -stim_file 6 ${base_dir}/derivatives/sub-${sub}/ses-${session}/step1_getmotion/${sub}.${session}.${task}.${run}.results/calculated_24_motion_params/${sub}_${task}_24_param.1D'[11]' -stim_base 6 \
		    -stim_file 7 ${base_dir}/derivatives/sub-${sub}/ses-${session}/step1_getmotion/${sub}.${session}.${task}.${run}.results/calculated_24_motion_params/${sub}_${task}_24_param.1D'[18]' -stim_base 7 \
		    -stim_file 8 ${base_dir}/derivatives/sub-${sub}/ses-${session}/step1_getmotion/${sub}.${session}.${task}.${run}.results/calculated_24_motion_params/${sub}_${task}_24_param.1D'[19]' -stim_base 8 \
		    -stim_file 9 ${base_dir}/derivatives/sub-${sub}/ses-${session}/step1_getmotion/${sub}.${session}.${task}.${run}.results/calculated_24_motion_params/${sub}_${task}_24_param.1D'[20]' -stim_base 9 \
		    -stim_file 10 ${base_dir}/derivatives/sub-${sub}/ses-${session}/step1_getmotion/${sub}.${session}.${task}.${run}.results/calculated_24_motion_params/${sub}_${task}_24_param.1D'[21]' -stim_base 10 \
		    -stim_file 11 ${base_dir}/derivatives/sub-${sub}/ses-${session}/step1_getmotion/${sub}.${session}.${task}.${run}.results/calculated_24_motion_params/${sub}_${task}_24_param.1D'[22]' -stim_base 11 \
		    -stim_file 12 ${base_dir}/derivatives/sub-${sub}/ses-${session}/step1_getmotion/${sub}.${session}.${task}.${run}.results/calculated_24_motion_params/${sub}_${task}_24_param.1D'[23]' -stim_base 12 \
		-regress_run_clustsim no			      \
		-regress_est_blur_epits                               \
		-regress_est_blur_errts

	./proc.${sub}_${session}_${task}_${run}
}

module unload afni
module load afni/19.0


sub=$1
session=$2
task=$3
run=$4
anat_path=$5
func_path=$6
base_dir=$7

analysis "$sub" "$session" "$task" "$run" "$anat_path" "$func_path" "$base_dir"


# try to make matrices right after preprocessing
cd /project2/mdrosenberg/ava/ava_pipeline/code/preprocessing/utils
python3 ./make_static_FC_matrices.py sub-${sub} ${session} ${task} ${run} ${base_dir}/derivatives/sub-${sub}/ses-${session}/step2_24motparam/${sub}.${session}.${task}.${run}.results/

# remove BRIK and HEAD files in step1_getmotion to save space
cd /project2/mdrosenberg/ava/ava_pipeline/code/preprocessing
python3 ./release_space.py ${base_dir}/derivatives/sub-${sub}/ses-${session}/step1_getmotion/${sub}.${session}.${task}.${run}.results
