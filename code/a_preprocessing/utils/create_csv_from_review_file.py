import subprocess
import os
from shutil import copyfile
import numpy as np
import pandas as pd

def get_sub_session(foldername):
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
    elif '_2.' in foldername:
        session = '02'
    return  sub, session


# grab a list of subject
# by reading all zipped files in the downloads folder
all_zipped = os.listdir('../../../zipped_sourcedata')
subject_sessions = [get_sub_session(x) for x in all_zipped]
subjects = [x[0] for x in subject_sessions]

sessions = ['01', '02']


def grab_motion(filename):
    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')

    latter = data.split('average motion (per TR)   : ')[1]
    motion = latter.split('max motion displacement')[0]
    return float(motion)


def grab_trs_censored(filename):
    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')

    latter = data.split('num TRs per run (censored): ')[1]
    motion = latter.split('fraction censored per run : ')[0]
    return float(motion)

def grab_censored_motion(filename):
    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')

    latter = data.split('average censored motion   :')[1]
    motion = latter.split('max motion displacement')[0]
    return float(motion)


def grab_num_TRS(filename):
    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')

    latter = data.split('num TRs per run           : ')[1]
    motion = latter.split('num TRs per run (applied)')[0]
    return float(motion)

def grab_frac_censored(filename):
    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')

    latter = data.split('fraction censored per run : ')[1]
    motion = latter.split('TRs total (uncensored)')[0]
    return float(motion)

data = {
'sub':[],
'session':[],
'task':[],
'run':[],
'motion':[],
}

def create_csv_from_review_file():
    motion_list = []
    for sub in subjects:
        for session in sessions:
            base = '/project2/mdrosenberg/ava/ava_pipeline/data/derivatives/'
            session_dir = f'{base}/sub-{sub}/ses-{session}/step2_24motparam'
            if os.path.exists(session_dir):
                files = os.listdir(session_dir)
                task_dirs = [i for i in files if 'results' in i]
                for task_dir in task_dirs:
                    task = task_dir.split('.')[2]
                    run = task_dir.split('.')[3]
                    ss_out_review = f'{session_dir}/{task_dir}/out.ss_review.{sub}.{session}.{task}.{run}.txt'
                    # print('ss_out_review path', ss_out_review)
                    if os.path.exists(ss_out_review):
                        motion = grab_motion(ss_out_review)
                        # num_trs = grab_num_TRS(ss_out_review)
                    else:
                        # print('missing:')
                        # print(ss_out_review)
                        num_trs = np.nan
                        motion = np.nan
                    data['motion'].append(motion)
                    data['session'].append(session)
                    data['task'].append(task)
                    data['sub'].append(sub)
                    data['run'].append(run)

    df = pd.DataFrame(data)
    df.to_csv('ss_out_review_compiled/ss_out_review_compiled.csv')
