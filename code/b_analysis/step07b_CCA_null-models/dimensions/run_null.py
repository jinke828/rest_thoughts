#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os
from sklearn import svm
from sklearn import metrics
import scipy.io
from scipy import stats
import matplotlib.pyplot as plt
from scipy import stats, linalg
import warnings
import math
import random
from sklearn.exceptions import ConvergenceWarning
def conv_r2z(r):
    with np.errstate(invalid='ignore', divide='ignore'):
        return 0.5 * (np.log(1 + r) - np.log(1 - r))
def conv_z2r(z):
    with np.errstate(invalid='ignore', divide='ignore'):
        return (np.exp(2 * z) - 1) / (np.exp(2 * z) + 1)
os.chdir('/gpfs/milgram/project/chun/jk2992/spontaneous_thoughts/') # change to your folder path

def reshape_FC(fc): # define a function to help read in FC data
    fc = np.transpose(fc,(2,0,1))
    fc = np.reshape(fc,(fc.shape[0],fc.shape[1]*fc.shape[2]))
    return fc

def get_num(string): # define a function to help read in behavioral data
    num = []
    for i in range(len(string)):
        if i % 5 == 2:
            num.append(int(string[i]))
    return num


import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--myvar', type=int, default=0)
args = parser.parse_args()

myvar = args.myvar
print(f"My variable is: {myvar}")

condition = 'd_beh_feat_selection'


# load FC
rest_FC = scipy.io.loadmat('./data/brain/rest_fc.mat')['rest'][0]
# delete 1032 s1r1 (response box error), index 29 because there is no 1004 and 1019
rest_FC[29] = np.delete(rest_FC[29],[0],axis = 0)
print('FC profiles shape: '+str(len(rest_FC))+'*'+str(rest_FC[2].shape))

nR = 268
nFC = int(nR*(nR-1)/2)

# prepare FC for each subject
nsubj = len(rest_FC)
FC_bysub = []
for i in range(nsubj):
    FC_bysub.append(reshape_FC(rest_FC[i]))

def prepare_null_beh(this_var): # define a function as a pipeline to prepare CAT data for training
    df = pd.read_csv('./data/beh/all_ratings.csv')
    beh_list = np.unique(df['Sub']) # create a behavioral participant list
    # print('We have '+str(len(beh_list)) + ' participants')
    # create a behavioral dataset by subject
    idx = -1
    beh_bysub = []
    for sub in range(len(beh_list)):
        sub_data = df[df['Sub']==beh_list[sub]][this_var]
        sub_vec = []
        # print(str(beh_list[sub]) + ': ' + str(len(sub_data)*8))
        for run in range(len(sub_data)):
            idx = idx + 1
            run_data = get_num(sub_data[idx])
            sub_vec.append(run_data)
        sub_vec = np.asarray(sub_vec)
        sub_vec = np.reshape(sub_vec,(sub_vec.shape[0]*sub_vec.shape[1]))
        # try zscore
        sub_vec = stats.zscore(sub_vec)
        random.shuffle(sub_vec)
        beh_bysub.append(sub_vec)

    # remove 1032 s1r1, 1044 s1r2
    beh_bysub[29] = np.delete(beh_bysub[29],range(0,8))
    beh_bysub[41] = np.delete(beh_bysub[41],range(8,16))

    # let's double check the brain match behavior
    count = 0
    for i in range(nsubj):
        if len(beh_bysub[i]) == FC_bysub[i].shape[1]:
            count = count + 1
    # if count == nsubj:
    #     print('All behavioral and brain data match')

    good_trial_bysub = []
    good_trial_id_bysub = []
    good_sub = []
    for sub in range(nsubj):
        sub_data = FC_bysub[sub]
        count = 0 
        good_trial_id = []
        for trial in range(sub_data.shape[1]):
            # a good trial has < 1000 missing FC (3 missing nodes)
            if np.sum(np.isnan(sub_data[:,trial])) < 1000:
                count = count + 1
                good_trial_id.append(trial)
        
        good_trial_bysub.append(count)
        # a good participant has > 20 good trials
        if count > 20:
            good_sub.append(sub)
            good_trial_id = np.transpose(good_trial_id)
            good_trial_id_bysub.append(good_trial_id)
    good_sub = np.transpose(good_sub)

    # select good participants
    nsubj_good = len(good_sub)
    FC_selected, beh_selected, mean_rating = [], [], []
    for i in range(nsubj_good):
        tmp_FC = FC_bysub[good_sub[i]]
        tmp_FC = tmp_FC[:,good_trial_id_bysub[i]]
        FC_selected.append(tmp_FC)
        
        tmp_beh = beh_bysub[good_sub[i]]
        tmp_beh = tmp_beh[good_trial_id_bysub[i]]    
        beh_selected.append(stats.zscore(tmp_beh)) # zscore again to make sure the mean is zero
        
    for i in range(nsubj_good):
        mean_rating.append(np.mean(beh_selected[i])) # to double check if the mean is indeed 0        

    # let's double check the brain match behavior
    count = 0
    count_trial = []
    for i in range(nsubj_good):
        if len(beh_selected[i]) == FC_selected[i].shape[1]:
            count = count + 1
            count_trial.append(len(beh_selected[i]))
    # if count == nsubj_good:
    #     print('All behavioral and brain data match -- 2nd check')
    ## add feature selection
    corrmat = np.zeros((nsubj_good,nFC))
    for sub in range(nsubj_good):
        print('running',sub+1,'/',nsubj_good)
        for feat in range(nFC):
            if np.any(np.isnan(beh_selected[sub])):
                tmp_r = 0
            else:
                tmp_r = get_r_omit_nan(FC_selected[sub][feat,:],beh_selected[sub])
            corrmat[sub,feat] = tmp_r

    training_edges = []
    for feat in range(nFC):
        [tval,pval] = scipy.stats.ttest_1samp(corrmat[:,feat],0)
        if pval < 0.05:
            training_edges.append(feat)
    print('selected edges:',len(training_edges))
        
    # reshape FC_selected
    training_FC = []
    training_beh = []
    for i in range(len(FC_selected)):
        for j in range(FC_selected[i].shape[1]):
            training_FC.append(FC_selected[i][:,j])
            training_beh.append(beh_selected[i][j])
    
    # one subject did not change the ratings for future and past.
    # Thus there are nan values in these two dimensions. Now removing these nans
    if this_var == 'Future' or this_var == 'Past':
        nanidx = np.where(np.isnan(training_beh))
        training_FC = np.delete(training_FC,nanidx,axis=0)
        training_beh = np.delete(training_beh,nanidx)

    training_FC = np.array(training_FC)[:,training_edges]
        
    # remove nans
    nanidx_trial = np.where(np.isnan(training_beh))
    training_FC = np.delete(training_FC,nanidx_trial,axis=0)
    training_beh = np.delete(training_beh,nanidx_trial)    
    
    nanidx_edges = np.where(np.isnan(training_FC))
    nanidx_edges1 = np.unique(nanidx_edges[0])
    nanidx_edges2 = np.unique(nanidx_edges[1])
    
    training_beh = np.delete(training_beh,nanidx_edges1)
    training_FC = np.delete(training_FC,nanidx_edges1,axis=0)
    training_FC = np.delete(training_FC,nanidx_edges2,axis=1)
    
    good_edges = np.delete(training_edges,nanidx_edges2)
    
    training_FC = np.asarray(training_FC)
    training_beh = np.asarray(training_beh)

    return training_FC, training_beh, good_edges, mean_rating


def modeling(fc,beh): # build a model for out-of-sample predictions
    # print('SVR prediction with model learned from CAT')
    # print('  train feature: '+str(fc.shape))
    # print('  train beh: '+str(beh.shape))

    clf = []
    clf = svm.SVR(kernel='rbf',max_iter=1000, gamma='auto')
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        clf.fit(fc, beh)
    # print('Training done!')
    return clf


def get_r_omit_nan(tc1,tc2):
    # get nan position
    nanidx = np.where(np.isnan(tc1))

    if len(tc1) - len(nanidx[0]) > 12:
        # remove nan from both tc
        tc1 = np.delete(tc1,nanidx)
        tc2 = np.delete(tc2,nanidx)
        # run correlation
        rval = stats.pearsonr(tc1,tc2)[0]
    else:
        rval = np.nan
    return rval


# In[ ]:

vars = ['Awake','External','Future','Past','Other','Valence','Image','Word','Detail']
vars_tosave = ['a_awake','b_external','c_future','d_past','e_other','f_valence','g_image','h_word','i_detail']
# load preprocessed resting-state FC data from HCP - averaged across rest runs for each subject
hcp = scipy.io.loadmat('./data/brain/net_hcp.mat')['NET']
print('loaded HCP FC shape: ', hcp.shape)
print('')

iterations = 5
for i in range(iterations):
    # if iter % 10 == 1:
    print('running',iter)
    all_vars = []
    for vi, var in enumerate(vars):
        train_fc, train_beh, edges, mean_rating = prepare_null_beh(var)
        print(mean_rating)
        model = modeling(train_fc,train_beh)
        all_subs = []
        for sub in range(hcp.shape[0]):
            this_sub = hcp[sub,edges].reshape(-1,1)
            predicted = model.predict(this_sub.T)
            all_subs.append(predicted)
        all_vars.append(np.array(all_subs))
    scipy.io.savemat('./results/CCA/dimensions/null'+str(myvar) + '_' +str(i)+'.mat',{'null':all_vars})

