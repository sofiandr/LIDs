# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 14:34:32 2023

        
        ''' 
        # To define start and end times I set as a baseline zero  and I check from valley time to before
        # 1 minute = 2000 samples which is the closest point that touches zero. same for valley 2 but for after 1 min
        # the reason I apply that to the filtered and not the raw data is because the anomalies in the raw sometimes as
        #the oscillation proceeded it touched zero before rising normally again up
        '''
     

@author: SOFIA
"""


def get_start_end_times(fils, peaks,w, val_times1, val_times2):
    import numpy as np
    amp = []
    start_times = []
    end_times = []
    
    for i in range(len(val_times1)):
        item = fils[peaks[i]] - fils[w[i]]
        amp.append(item)
        st = np.where(fils == min(fils[int(val_times1[i]*2000-2000):int(val_times1[i]*2000)], key=abs))
        start_times.append(st[0][0]/2000)
        st = np.where(fils == min(fils[int(val_times2[i]*2000):int(val_times2[i]*2000+2000)], key=abs))
        end_times.append(st[0][0]/2000)
    
    return start_times, end_times