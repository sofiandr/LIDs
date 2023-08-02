# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 14:03:20 2023

@author: SOFIA
"""

# config.py

# Global variables
Mo = 'Mo-0100-ER-Tam'

use_classifier=1   # we are also feeding the detected for more cleaning into an svm model , if you dont want to use the svm classier put 0 here

rec_folders_start=10
channels=32   # this can be a number for example 32 or 10 if you want the first 10 channels but it can also be an array ie [2:5] when you want to be more specific on the ch selection for the detection



peaks_height_thres= (450,2000)
valley_height_thres= (100,1300)

prominence=550

# Detection parameters
#detection_threshold = 0.5

model_path= '/home/sofiand/Code/eiids/Detection/bare_minum_from_scratch/trained_model.pkl'

