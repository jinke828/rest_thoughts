analysis () {

# set variables and data directories
sub=$1
session=$2
datatype=$3
run=$4
anat_path=$5
func_path=$6
base_dir=$7



mkdir -p ${base_dir}/derivatives/sub-${sub}/ses-${session}/first_pass
cd ${base_dir}/derivatives/sub-${sub}/ses-${session}/first_pass

echo ${base_dir}/derivatives/sub-${sub}/ses-${session}/first_pass


# run afni_proc.py to create a single subject processing script
# created by uber_subject.py: version 0.39 (March 21, 2016)
# creation date: Fri Apr  7 12:11:05 2017
afni_proc.py -subj_id ${sub}.${session}.${datatype}.${run}                                  \
	-script proc.${sub}_${session}_${datatype}_${run} -scr_overwrite                  \
	-blocks despike tshift align tlrc volreg blur mask regress  \
	-copy_anat ${anat_path}          \
	-dsets ${func_path}    \
	-tcat_remove_first_trs 3                              \
	-align_opts_aea -cost lpc+ZZ -giant_move              \
	-tlrc_base MNI_avg152T1+tlrc                          \
	-tlrc_NL_warp					      \
	-volreg_align_to MIN_OUTLIER                          \
	-volreg_align_e2a                                     \
	-volreg_tlrc_warp                                     \
	-mask_segment_anat yes                                \
	-mask_segment_erode yes                               \
	-regress_bandpass 0.01 0.1                            \
	-regress_ROI WMe brain                          \
	-regress_apply_mot_types demean deriv                 \
	-regress_est_blur_epits                               \
	-regress_est_blur_errts                               \
	-regress_run_clustsim yes

	./proc.${sub}_${session}_${datatype}_${run}
}

module load afni/19.0

sub=$1
session=$2
datatype=$3
run=$4
anat_path=$5
func_path=$6
base_dir=$7


analysis "$sub" "$session" "$datatype" "$run" "$anat_path" "$func_path" "$base_dir"
