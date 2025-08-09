#!/usr/bin/env python
# coding: utf-8

# In[2]:


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
import random
from sklearn.exceptions import ConvergenceWarning
os.chdir('/gpfs/milgram/project/chun/jk2992/spontaneous_thoughts/')  # change to your folder path


# ## Predicting 9 thought dimensions

# In[5]:

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--myvar', type=int, default=0)
args = parser.parse_args()

myvar = args.myvar
print(f"My variable is: {myvar}")

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

# load FC
rest_FC = scipy.io.loadmat('./data/brain/rest_fc.mat')['rest'][0]
# delete 1032 s1r1 (response box error), index 29 because there is no 1004 and 1019
rest_FC[29] = np.delete(rest_FC[29],[0],axis = 0)
print('FC profiles shape: '+str(len(rest_FC))+'*'+str(rest_FC[2].shape))

# prepare FC for each subject
nsubj = len(rest_FC)
FC_bysub = []
for i in range(nsubj):
    FC_bysub.append(reshape_FC(rest_FC[i]))

# load FC again
rest_FC = scipy.io.loadmat('./data/brain/rest_fc.mat')['rest'][0]
# aligning FCs and topics by trial
fake_run = np.empty((1,8,35778)) # create a np.nan run for sub 1044 s1r2
fake_run[:] = np.nan
rest_FC[41] = np.vstack((rest_FC[41][0,:,:].reshape(1,8,35778),fake_run,rest_FC[41][1:,:,:]))

FC_bytrial = np.hstack((reshape_FC(rest_FC[0]),reshape_FC(rest_FC[1])))
for sub in range(2,len(rest_FC)):
    FC_bytrial = np.hstack((FC_bytrial,reshape_FC(rest_FC[sub])))

# QC on trials
df = pd.read_csv('./data/beh/topics.csv')
good_trial_id,good_fc,good_topic = [], [], []
for i in range(FC_bytrial.shape[1]):
    this_fc = FC_bytrial[:,i]
    this_topic = df['Topics'].tolist()[i]
    if sum(np.isnan(this_fc)) > 1000 or np.isnan(this_topic) or this_topic == 3 or this_topic == 9: # remove the CAT movies
        pass
    else:
        good_trial_id.append(i)
        good_fc.append(this_fc)
        good_topic.append(this_topic)

# further QC on FCs
good_fc = np.asarray(good_fc)
train_fc, good_edge = [], []
for i in range(good_fc.shape[1]):
    this_fc = good_fc[:,i]
    if np.any(np.isnan(this_fc)):
        pass
    else:
        good_edge.append(i)
        train_fc.append(this_fc)

train_fc = np.asarray(train_fc)
train_fc.shape


# In[13]:


# Import train_test_split function
from sklearn.model_selection import train_test_split
#Import svm model
from sklearn import svm
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
from imblearn.over_sampling import SMOTE, ADASYN

#Create a svm Classifier
clf = svm.SVC(kernel='rbf', probability=True) # Linear Kernel

# Split dataset into training set and test set
X_train = train_fc.T
y_train = good_topic

niter = 25
for i in range(niter*(myvar-1),niter*myvar):
    random.shuffle(y_train)
    
    X_resampled, y_resampled = SMOTE().fit_resample(X_train, y_train) # over sample 
    
    #Train the model using the training sets
    clf.fit(X_resampled, y_resampled)
    
    
    hcp = scipy.io.loadmat('./data/brain/net_hcp.mat')['NET']
    print('loaded HCP FC shape: ', hcp.shape)
    
    test_fc = hcp[:,good_edge].T
    print('HCP data shape for model testing:',test_fc.T.shape)
    
    predicted_beh = []
    for sub in range(test_fc.shape[1]):
        this_sub = test_fc[:,sub].reshape(-1,1)
        predicted = clf.predict_proba(this_sub.T)
        predicted = np.array(predicted[0])
        predicted_beh.append(predicted)
    
    scipy.io.savemat('./results/CCA/topics/null'+str(myvar) + '_' +str(i)+'.mat',{'null':predicted_beh})
    print('Successfully saved!')




