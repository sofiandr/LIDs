# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 13:54:34 2023

_____

load_data :
    gets the data .mat files and extracts the lfp recording

@author: SOFIA
"""

# load_data.py
import numpy as np
import mat73
import scipy.io

def load_data(day, channel, Mo):
    path = "/nfs/turbo/lsa-ojahmed/Projects/TamoxifenExperiments/processedData/" + str(Mo) + "/" + str(day) + "/downsampled/resampled_csc" + str(channel) + ".mat"
    try:
        x = mat73.loadmat(path)
        s = x.get('LFP')
        
        
        # i dont know why sometimes i couldnt use mat73 and it worked with scipy
    except:
        x = scipy.io.loadmat(path)
        s = x.get('LFP')
        s = np.concatenate(s, axis=0)

    return s