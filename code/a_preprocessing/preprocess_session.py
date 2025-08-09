import subprocess
from py7zr import unpack_7zarchive
import shutil
import os
from pathlib import Path
from argparse import ArgumentParser
from preprocess_scan import preprocess_scan
from nilearn import image, plotting
from nilearn.plotting import plot_epi, show
from nilearn.image.image import mean_img

def get_sub_session(foldername):
    print(foldername)
    foldername = foldername.lower()
    if '_' in foldername:
        save_split = foldername.split('ava_')
        sub = foldername.split('ava_')[1]
        sub = sub.split('_')[0]
        sub  = sub.split('.')[0]
    else:
         sub = '1002'

    session = '01'
    if 's2' in foldername:
        session = '02'
    elif '_2_' in foldername:
        session = '02'
    elif '_2' in foldername:
        session = '02'
    return  sub, session

base_dir = '/project/mdrosenberg/ava/ava_pipeline/data'



def preprocess_session(foldername):
    sub, session = get_sub_session(foldername)

    # move everything into data dir
    new_data_dir = f'/project/mdrosenberg/ava/ava_pipeline/data/sub-{sub}/ses-{session}'
    anat_dir, func_dir = f'{new_data_dir}/anat', f'{new_data_dir}/func'
    Path(anat_dir).mkdir(parents=True, exist_ok=True)
    Path(func_dir).mkdir(parents=True, exist_ok=True)

    # # move anatomical file
    print('begin moves', sub,session, flush=True)
    anat_file = [i for i in os.listdir(f'/project/mdrosenberg/ava/ava_pipeline/sourcedata/{foldername}') if 'MPRage' in i and 'nii' in i][0]
    current_anat_path = f'/project/mdrosenberg/ava/ava_pipeline/sourcedata/{foldername}/{anat_file}'
    shutil.copy2(current_anat_path,
                 f'{anat_dir}/sub-{sub}_ses-{session}_acq-MPRAGE_run-01_T1w.nii.gz')

    for task in [
                 'avNW', # this is north by northwest
                 'avCake', # this is the cake video
                 'aNT', # this is the pie audio
                 'vNT' # this is the croissant vid
                 ]:
        func_files = [i for i in os.listdir(f'/project/mdrosenberg/ava/ava_pipeline/sourcedata/{foldername}') if task.lower() in i.lower()]
        func_files = [i for i in func_files if '.nii' in i]
        if len(func_files) > 0:
            func_file = func_files[0]
            current_func_path = f'/project/mdrosenberg/ava/ava_pipeline/sourcedata/{foldername}/{func_file}'

            # setting the run number
            if task == 'rest1':
                task, run = 'rest', '01'
            elif task == 'rest2':
                task, run = 'rest', '02'
            else: # we only have 1 run of all other tasks
                run = '01'

            shutil.copy2(current_func_path,
                         f'{func_dir}/sub-{sub}_ses-{session}_task-{task}_run-{run}_bold.nii.gz')


            # out_folder = f'../../data/derivatives/sub-{sub}/ses-{session}/'
            # ss_out_path = f'{sub}.{session}.{task}.{run}.results/out.ss_review.{sub}.{session}.{task}.{run}.txt'
            # out_file_first_pass = f'{out_folder}/first_pass/{ss_out_path}'
            # out_file_24motparam = f'{out_folder}/24motparam/{ss_out_path}'
            # netts_file_out = f'{out_folder}/24motparam/{sub}_{session}_{task}_{run}_LPI_000.netts'
            # if the netts file is there, the subject is done
            # otherwise some job needs to be started
            # start_at = 'fc_mat'
            # if not os.path.exists(netts_file_out):
            #     if not os.path.exists(out_file_first_pass):
            #         start_at = 'first_pass'
            #     elif not os.path.exists(out_file_24motparam):
            #         start_at = '24motparam'

            start_at = 'step1_getmotion'
            # after moving each functional scan,
            # we kick of preprocessing for that functional scan
            print(f'Preprocess one session: {sub}, {task}, {session}, {start_at}',
                  flush=True)
            preprocess_scan(sub=sub,
    						  session=session,
    						  task=task,
    						  run=run,
                              start_at=start_at,
    						  base_dir=base_dir)

     # ************** commenting this out, for debug
    # remove sourdata folder at the end of kicking of jobs and moving everything
    # to data folder
    # print('removing data from sourcedata')
    # shutil.rmtree(f'../../sourcedata/{foldername}')
    # print('removed data from sourcedata')

if __name__ == "__main__":
    sessions = [
    # 'AVA_1001_sess1',
    # 'AVA_1002_sess1',
    # 'AVA_1003_sess1',
    # 'AVA_1003_sess2',
    # 'AVA_1005_sess1',
    # 'AVA_1005_sess2', 
    # 'AVA_1006_sess1',
    # 'AVA_1006_sess2', 
    # 'AVA_1007_sess1',
    # 'AVA_1007_sess2', 
    # 'AVA_1008_sess1',
    # 'AVA_1008_sess2', 
    # 'AVA_1009_sess1',
    # 'AVA_1009_sess2', 
    # 'AVA_1010_sess1',
    # 'AVA_1010_sess2',
    # 'AVA_1011_sess1',
    # 'AVA_1011_sess2', 
    # 'AVA_1012_sess1',
    # 'AVA_1012_sess2', 
    # 'AVA_1013_sess1',
    # 'AVA_1013_sess2', 
    # 'AVA_1014_sess1',
    # 'AVA_1014_sess2',
    # 'AVA_1015_sess1', 
    # 'AVA_1015_sess2',
    # 'AVA_1016_sess1',
    # 'AVA_1016_sess2', 
    # 'AVA_1017_sess1',
    # 'AVA_1017_sess2',
    # 'AVA_1018_sess1', 
    # 'AVA_1018_sess2',
    # 'AVA_1020_sess1'

    
    # 'AVA_1021_sess1', 
    # 'AVA_1021_sess2',
    # 'AVA_1022_sess1',
    # 'AVA_1022_sess2',
    # 'AVA_1023_sess1',
    # 'AVA_1023_sess2',
    # 'AVA_1024_sess1',
    # 'AVA_1024_sess2', 
    # 'AVA_1025_sess1',
    # 'AVA_1025_sess2',  
    # 'AVA_1026_sess1',
    # 'AVA_1026_sess2', 
    # 'AVA_1027_sess1',
    # 'AVA_1027_sess2', 
    # 'AVA_1028_sess1',
    # 'AVA_1028_sess2', 
    # 'AVA_1029_sess1',
    # 'AVA_1029_sess2', 
    # 'AVA_1030_sess1',
    'AVA_1030_sess2',
    # 'AVA_1031_sess1',
    # 'AVA_1031_sess2',
    # 'AVA_1032_sess1',
    # 'AVA_1032_sess2',
    # 'AVA_1033_sess1',
    # 'AVA_1033_sess2',
    # 'AVA_1034_sess1',
    # 'AVA_1034_sess2',
    # 'AVA_1035_sess1',
    # 'AVA_1035_sess2',
    # 'AVA_1036_sess1',
    # 'AVA_1036_sess2',
    # 'AVA_1037_sess1',
    # 'AVA_1037_sess2',
    # 'AVA_1038_sess1',
    # 'AVA_1038_sess2',
    # 'AVA_1039_sess1',
    # 'AVA_1039_sess2',
    # 'AVA_1040_sess1',
    # 'AVA_1040_sess2'


    # 'AVA_1041_sess1',
    # 'AVA_1041_sess2',
    # 'AVA_1042_sess1',
    # 'AVA_1042_sess2',
    # 'AVA_1043_sess1',
    # 'AVA_1043_sess2',
    # 'AVA_1044_sess1',
    # 'AVA_1044_sess2',
    # 'AVA_1045_sess1',
    # 'AVA_1045_sess2',
    # 'AVA_1046_sess1',
    # 'AVA_1046_sess2',
    # 'AVA_1047_sess1',
    # 'AVA_1047_sess2',
    # 'AVA_1048_sess1',
    # 'AVA_1048_sess2',
    # 'AVA_1049_sess1',
    # 'AVA_1049_sess2',
    # 'AVA_1050_sess1',
    # 'AVA_1050_sess2',
    # 'AVA_1051_sess1',
    # 'AVA_1051_sess2',
    'AVA_1052_sess1',
    # 'AVA_1052_sess2',
    # 'AVA_1053_sess1',
    # 'AVA_1053_sess2',
    # 'AVA_1054_sess1',
    # 'AVA_1055_sess1',
    # 'AVA_1055_sess2',
    # 'AVA_1056_sess1',
    # 'AVA_1056_sess2',
    # 'AVA_1057_sess1',
    # 'AVA_1057_sess2',
    # 'AVA_1058_sess1',
    # 'AVA_1058_sess2',
    # 'AVA_1059_sess1',
    # 'AVA_1059_sess2',
    # 'AVA_1060_sess1',
    # 'AVA_1060_sess2',
    # 'AVA_1061_sess1',
    # 'AVA_1061_sess2',
    # 'AVA_1062_sess1',
    # 'AVA_1062_sess2'
    ]
    for folder in sessions:
        preprocess_session(folder)
