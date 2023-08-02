# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 16:28:26 2023


@author: SOFIA

_________
rec_folders:
    when you want to dectet multiple recording from multiple days for one mouse this
    help you define what days you want based on the directory of the days folders
    saved on Rec_Info.csv for every mouse.
    
    that helped eith the lab's recording data structure.
    
    You can use signle days too
    
________


"""

import pandas as pd



def rec_folders(Mo, rec_folders_start):
   
   
    folders=pd.read_csv('/nfs/turbo/lsa-ojahmed/Sofia/eIIDs/Analysis/' + str(Mo) + '/Rec_Info.csv') 
    
    folders=folders.sort_values(by=["Var3"], ascending=False)  
    folders=folders.get("Var3")
    folders=folders[rec_folders_start:]   
    print(folders) 
    
    return folders