import pandas as pd
import os
from create_csv_from_review_file import create_csv_from_review_file


# this script does 3 things
# 1. it updates ss_out_review_compiled.csv (which gives an overview of motion etc for all prepprocessed scans)
# 2. it spits out what sessions still need to be preprocessed
# 3. it spits out a csv which contains only subs that might be missing a run

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
    elif '_2' in foldername and foldername.endswith('_2'):
        session = '02'

    return  sub, session


# LOAD UP LIST OF SESSIONS

# load up all subs we've downloaded from the MRIRC server
all_zipped = os.listdir('../../../zipped_sourcedata')
subs_we_want = [get_sub_session(x) for x in all_zipped]
subs_we_want = [x[0]+ '_'+x[1] for x in subs_we_want]

# first update the csv in case there are new sessions that have been preprocessed
create_csv_from_review_file()

# load up all subs we've preprocessed by reading in our combined csv (made above)
df = pd.read_csv('ss_out_review_compiled/ss_out_review_compiled.csv')
df['sub_session'] = df['sub'] +'_0'+ df['session'].astype(str)
subs_we_have = list(df['sub_session'].value_counts().keys())



# CHECK FOR DUPLICATE DOWNLOADS

# print any dupes - ie for some reason there are 2 zip files for this session
# (sometimes the file is saved as .zip and as .7s, sometimes there was some error )
dupes = set([x for x in all_zipped if all_zipped.count(x) > 1])
print('dupe zips', dupes)


# CHECK FOR SESSIONS THAT NEED TO BE PREPROCESSED

# compare subs we have vs subs we want
print('number of sessions to be preprocessed', len(set(subs_we_want) - set(subs_we_have)))

all_converted_to_nifti = [x for x in os.listdir('../../../sourcedata') if 'AVA' in x or 'ava' in  x]
subs_converted = [get_sub_session(x) for x in all_converted_to_nifti]
subs_converted = [x[0]+ '_'+x[1] for x in subs_converted]

# separate missing subs into those that need to be converted then preprocessed
# vs just preprocessed
missing_sessions = list(set(subs_we_want) - set(subs_we_have))
sessions_to_be_converted = set(missing_sessions) - set(subs_converted)
sessions_to_be_preprocessed = set(missing_sessions) - set(sessions_to_be_converted)

# print sessions that need to be preprocessed
print('sessions to be converted to nfiti THEN preprocessed', sessions_to_be_converted)
print('sessions to be preprocessed', sessions_to_be_preprocessed)


# CHECK FOR RUNS WITHIN A SESSION THAT ARE MISSING!
def get_missing_runs():
    df = pd.read_csv('ss_out_review_compiled/ss_out_review_compiled.csv')
    df['task_run'] = df['task'] + '_' +df['run'].astype(str)

    data = {'sub': [],  'session': [],'task_runs':[]}
    for sub in df['sub'].unique():
        for session in [1, 2]:
            subset = df[(df['sub']==sub) & (df['session']==session)]
            task_runs = subset.task_run.unique()
            if len(task_runs) < 5:
                data['sub'].append(sub)
                data['session'].append(session)
                data['task_runs'].append(task_runs)

#                 to_concat.append(subset)

    missing_runs = pd.DataFrame(data)
    missing_runs  = missing_runs[~missing_runs['sub'].str.contains('pilot')]
    return missing_runs

missing_runs  = get_missing_runs()
missing_runs.to_csv('sessions_with_missing_runs.csv')
