# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 14:03:47 2023

create the whole eiids detection project in an improved 
architcture for easy changes and updates.

Rather than using an one page script.

This will be upload to github and planning on using that on great lakes by cloning
the rep.

_____________________

main:
    
    calling all the other functions and performs everything
    
    
    
default: this will detect all LIDs for all 32 channels for Mo_100 all days in rec info
you can change that by changins params in config file.

!!!! The directories in this are from Turbo and weere accessed by University of Michigan's cluster "Great Lakes" 
If you want to work locally you have to change directory !!!!!!


svm classifier is going to be used default, if you dont want to use it change 1 to 0 in the config file

@author: SOFIA
"""

# main.py


import config    # first check config if you want to define different parameters


# import all other functions 

from rec_folders import rec_folders
from load_data import load_data
from detect_lids import detect_lids
from classifier_svm import classifier_svm
import sys
import os
import scipy
import logging





def main(use_classsier= config.use_classifier):
    
    #get the recording days of the mouse
    days= rec_folders(config.Mo, config.rec_folders_start)
    
    channels=config.channels
    model_path= config.model_path
    
    for i in days:
        for j in channels:
            
            # get the lfp
            s= load_data(i,j,config.Mo)
            
            # Call the detect_iids function 
            # note: the artifact rejection is being called in the detect_lids function, if you need to change something there
            # saves the morphological param LIDs in a df and mat files of them of 10 sec filteres and raw
            df,iids,iidsFiltered = detect_lids(s,i,j, config.Mo,  config.peaks_height_thres, config.valley_height_thres, config.prominenece)
            
            
            # Feed those LIDs to our trained SVM model to reject false positives if config.use_classifier = 1
            if config.use_classifier:
                classifier_svm(j,df,iids,iidsFiltered,model_path)
        
        
            
            
            
            
            
            
            
            

if __name__ == "__main__":
    try:
        
        main(use_classsier=config.use_classifier)
    
    
    except BaseException:
        
        logging.exception("The following exception was thrown:")
        saveto="/nfs/turbo/lsa-ojahmed/Sofia/eIIDs/Analysis/Problem_Logs/"+ config.Mo+ "/" + config.day+"/"
        if not os.path.exists(saveto):
                                      os.makedirs(saveto)
        
        os.chdir(saveto)
        text= 'An error for this redording file occured, probably one or more channels recording were not found or no iids detected\n you can take a look in the specific recording files in the Projects directory'
        print(text)
        with open('error.txt', 'a') as f:
                                       f.write(text)
        exit
     
        
         
    
    def excepthook(exc_type, exc_value, exc_traceback):
        with open('exception.txt', 'w') as f:
            f.write(f"Exception Type: {exc_type}\n")
            f.write(f"Exception Value: {exc_value}\n")
            f.write("Traceback:\n")
            
    
    sys.excepthook = excepthook






