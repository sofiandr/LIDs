# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 14:02:41 2023



______
detect_lids.py:
    basic first detection based on filtering on spec freqs, find_peaks and creating LID pairs between valley 1 - peak - valley 2
    
    
    The parameters for thresholds on peaks, valleys , prominece were decided upon checking distributions on detection examples for various number ranges
    
@author: SOFIA
"""

# detect_iids.py

import numpy as np
from scipy.signal import find_peaks
from find_closest import find_closest
from artifacts_rejec import artifact_rejec
from get_start_end_times import get_start_end_times
import sys 
import os
import pandas as pd
import scipy.io 

def detect_lids(s,day, channel, Mo, peaks_height_thres, valleys_height_thres, prominence):
    
    from butter_filter import butter_bandpass_filter

   
    fs = 2000
    t = np.arange(s.size) / fs

    # Filter the signal between 0.1-2 Hz
    filtered_signal = butter_bandpass_filter(s, 0.1, 2, 2000, order=2)
    
    '''
    # the following is checking z score for determinate the thresholds but we are dealing with 24/7 lfp recording so this takes EXTREMELY too much time to compute 
    # I left the code here in case it is to be used for smaller duration lfps
    
    # fils=gaussian_filter1d(s, 100)
    # I apply the normalisation of filtered signla to get rid of the huge artifact amplitudes

    # zscored=stats.zscore(fils)
    # sigma= stat.stdev(fils)
    # mi=stat.mean(fils)

    # after observations I checked I want to set the threshold for 2z so the ampitude value would be:

    # thres= sigma * 2 + mi
    # print(thres)

    # fils=stats.zscore(fils)
    # plt.plot(fils)
    '''
    
     
    # Find peaks and valleys on the filtered and not on the raw signal a there it d be a mess because of the lack of smoothiness
    
    peaks, _ = find_peaks(filtered_signal, height=peaks_height_thres, prominence=prominence)
    val, _ = find_peaks(filtered_signal * -1, height=valleys_height_thres, prominence=prominence)

    # Find times of peaks and vallesys and group them
    
    
    for i in peaks:
        
        peak_times=t[0] +peaks/fs  #peaks time in seconds
        val_times=t[0]+ val/fs
    
  
    ##match before and after valley to peak     
         
    # help arrays                                  
    tes=list()
    tes2=list()
    
    for i in range( len(peak_times) ):
        tes, tes2= find_closest(val_times, peak_times[i],i,peak_times, tes, tes2)       # using find_closest , check .py file if needed
    
    w1=val[tes]
    w=val[tes2]
    
    peak_times=peak_times[peak_times != 0]  
    peaks=peaks[peaks != 0]
      
    
    for i in peaks:
        # time in seconds
        val_times1=t[0]+ w/fs
        val_times2=t[0]+ w1/fs
            
            
            
    # basic rejection of > 3000 ampl events
    for i in range(len(peaks)):

        if any(abs(s[w[i]-2000:w1[i]+2000]) > 3000):
            # print('artifact')
            w[i] = 0
            w1[i] = 0
            peaks[i] = 0
            val_times1[i] = 0
            val_times2[i] = 0
            peak_times[i] = 0

    # delete zeros from all arrays
    peak_times = peak_times[peak_times != 0]
    peaks = peaks[peaks != 0]

    w = w[w != 0]
    w1 = w1[w1 != 0]

    val_times1 = val_times1[val_times1 != 0]
    val_times2 = val_times2[val_times2 != 0]
    
    # get start - end times
    start_times, end_times = get_start_end_times(filtered_signal, peaks,w, val_times1, val_times2)
    
    
    # save LIDs dor 10 seconds both for raw and filtered as .mat files

    iids = list()
    iidsFiltered = list()
    for i in range(len(peaks)):
        y = s[peaks[i]-10000: peaks[i]+10000]
        y1 = filtered_signal[peaks[i]-10000: peaks[i]+10000]
        iids.append(y)
        iidsFiltered.append(y1)

    # gather evrything in a Dataframe from a dictionary
    specs = {'start_time': start_times, 'end_time': end_times, 'peak_time': peak_times, 'start_valley_times': val_times1,
             'end_valley_times': val_times2, 'peak_ampl': filtered_signal[peaks], 'start_val_ampl': filtered_signal[w], 'end_val_ampl': filtered_signal[w1],
             'duration': np.subtract(end_times, start_times), 'dur from start to peak': np.subtract(peak_times, start_times),
             'dur from peak to end': np.subtract(end_times, peak_times), 'dur from v1 to peak': np.subtract(peak_times, val_times1),
             'dur from start v1 to v2': np.subtract(val_times2, val_times1)}

    df = pd.DataFrame(data=specs)
    
    initial_size = len(df)
    print("Initial size of df:", initial_size, file=sys.stdout)
    
    # Sort by 'peak_ampl' in descending order
    df = df.sort_values('peak_ampl', ascending=False)
            
    #  perform artifact rejection 
    df, initial_indexes= artifact_rejec( initial_size, df)
    
    
    ''' !!!!!! SAVE KEEP ONLY THOSE INDEXES ALSO IN THE .MAT FILE CONTAINING THE EIIDS - CLEAN THE EIIDS - '''
    
   
    
    # Get the remaining indexes after deleting rows from the DataFrame
    remaining_indexes = df['original_index'].tolist()
    
    # Identify the deleted indexes by finding the set difference
    deleted_indexes = np.setdiff1d(initial_indexes, remaining_indexes)
 


# Update iids list to only contain the elements corresponding to the remaining indexes
# iids = [iids[i] for i in remaining_indexes]

    # change the directory so I don't need to put the savepath over and over again everywhere

    saveto = "/nfs/turbo/lsa-ojahmed/Sofia/eIIDs/Analysis/final_detection_with_ML_dur10sec/" + Mo + "/" + day+"/"
    if not os.path.exists(saveto):
        os.makedirs(saveto)

    os.chdir(saveto)

  
    df.to_csv("eIIDss_char_ch" + str(channel) + ".csv")  # , sep='\t')
    print('Saved CSV!', file=sys.stdout)

    # Update the list 'A' to only contain the elements corresponding to the remaining indexes
    iids = [iids[i] for i in remaining_indexes]
    iidsFiltered = [iidsFiltered[i] for i in remaining_indexes]

    scipy.io.savemat("eIIDs_ch" + str(channel) +
                     ".mat", mdict={'eiids': iids})
    print('Saved .mat files')
    scipy.io.savemat("eIIDsFiltered_ch" + str(channel) +
                     ".mat", mdict={'eiidsFilt': iidsFiltered})
    
    scipy.io.savemat("Indexes_deleted" + str(channel) +
                     ".mat", mdict={'ind': deleted_indexes})
    
    
    


    return df,iids,iidsFiltered

