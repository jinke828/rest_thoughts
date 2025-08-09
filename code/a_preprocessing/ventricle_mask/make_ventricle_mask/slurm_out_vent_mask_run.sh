Note that the current default version of R is 3.6.1.
/project2/mdrosenberg/ava/data//derivatives/sub-pilot001/ses-01/first_pass
** missing run 1 dataset: /project2/mdrosenberg/ava/data//pilot001/func/pilot001_task-aNT_run-01_bold.nii.gz
----------------------------------------------------------------------
** failed command (create_blocks):

  afni_proc.py -subj_id pilot001.01.aNT.01 -script proc.pilot001_01_aNT_01                \
      -scr_overwrite -blocks despike tshift align tlrc volreg blur mask                   \
      regress -copy_anat                                                                  \
      /project2/mdrosenberg/ava/data//pilot001/anat/pilot001_acq-MPRAGE_run-01_T1w.nii.gz \
      -dsets                                                                              \
      /project2/mdrosenberg/ava/data//pilot001/func/pilot001_task-aNT_run-01_bold.nii.gz  \
      -tcat_remove_first_trs 3 -align_opts_aea -cost lpc+ZZ -giant_move                   \
      -tlrc_base MNI_avg152T1+tlrc -tlrc_NL_warp -volreg_align_to MIN_OUTLIER             \
      -volreg_align_e2a -volreg_tlrc_warp -mask_segment_anat yes                          \
      -mask_segment_erode yes -regress_bandpass 0.01 0.1 -regress_ROI WMe                 \
      brain -regress_apply_mot_types demean deriv -regress_est_blur_epits                 \
      -regress_est_blur_errts -regress_run_clustsim yes
----------------------------------------------------------------------
preprocessing_vent.sh: line 44: ./proc.pilot001_01_aNT_01: No such file or directory
