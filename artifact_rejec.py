# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 18:35:44 2023

___________
really important file containing all the artifact rej functions.
threshodls and params based on distributions after various observations and test for 5 SCN8A mutation mice
( Mo 100, Mo 269, Mo 282, Mo 290, Mo 296 )

artfact rejection:
    
    
    rejects possible duplciates, 
    possible pivots ( meaning two valleys matches same start and end times and count as 2 LIDs)
    Remove rows with V1 or V2 > 1.5 * peak_ampl
    removing rows based on duration (keeps only between 3-10 sec)
    removing rows based on valleys to peak duration  ratio and angles [mask= ( df['ratio']  > 1.6 )| (df['ratio'] < 0.35) | (df['tanv1'] < 400)| (df['tanv1'] >4000) |  (df['tanv2']<250) | ( df['tanv2']> 1500 ) ]
    
    
    
    
@author: SOFIA
"""
import sys
import numpy as np
def artifact_rejec(initial_size, df):

    # Remove duplicate rows based on 'start_valley_times'
    df = df.drop_duplicates(subset='start_valley_times', keep='first')
    
    
    
    # Print the size of df after removing duplicates
    after_duplicates_size = len(df)
    reduction_percentage_duplicates = (initial_size - after_duplicates_size) / initial_size * 100
    print("\nSize of df after removing duplicates:", after_duplicates_size, file=sys.stdout)
    print("Reduction percentage after removing duplicates:", reduction_percentage_duplicates, file=sys.stdout)
    
    
    
    
    
    # Add 'original_index' column and sort by 'original_index'
    df['original_index'] = df.index
    df = df.sort_values('original_index')
    
    initial_indexes = df['original_index'].tolist()
    
    # Remove pivots
    
    # Calculate the differences between consecutive elements in the 'start_time' column
    differences = np.diff(df['start_time'])
    
    # Create a boolean mask for rows where the difference is <= 2
    mask = np.concatenate(([True], differences <= 3))
    
    # Invert the mask
    mask_inverse = ~mask
    
    # Filter out the rows from the DataFrame based on the inverted mask
    df = df[mask_inverse].copy()
    
    # Reset the index of the filtered DataFrame
    df.reset_index(drop=True, inplace=True)
    
    # Print the size of df after removing pivots
    after_pivots_size = len(df)
    reduction_percentage_pivots = (after_duplicates_size - after_pivots_size) / after_duplicates_size * 100
    print("\nSize of df after removing pivots:", after_pivots_size, file=sys.stdout)
    print("Reduction percentage after removing pivots:", reduction_percentage_pivots, file=sys.stdout)
    
    # Remove rows with V1 or V2 > 1.5 * peak_ampl
    
    # Create a boolean mask based on the condition
    
    mask = (abs(df['start_val_ampl']) > 1* df['peak_ampl']) | (abs(df['end_val_ampl']) > 1 * df['peak_ampl']) 
    # Apply the mask to filter the DataFrame
    df = df[~mask]
    
    # Reset the index of the filtered DataFrame
    df.reset_index(drop=True, inplace=True)
    
    # Print the size of df after removing rows with V1 or V2 > 1 * peak_ampl
    after_peak_size = len(df)
    reduction_percentage_peak = (after_pivots_size - after_peak_size) / after_pivots_size * 100
    print("\nSize of df after removing rows with V1 or V2 > 1 peak_ampl or :", after_peak_size, file=sys.stdout)
    print("Reduction percentage after removing rows with V1 or V2 > 1peak_ampl", reduction_percentage_peak, file=sys.stdout)
    
    # Remove rows based on duration
    

    mask = (df['duration'] > 10) | (df['duration'] < 3)


    # Apply the mask to filter the DataFrame
    df = df[~mask]
    df.reset_index(drop=True, inplace=True)
    # Filter the DataFrame based on z-score conditions
    #df = df[(df['duration_zscore'] >= -1.5) & (df['duration_zscore'] <= 1.5)]  # 1.5
    
    after_duration_size = len(df)
    reduction_percentage_duration = (after_peak_size - after_duration_size) / after_peak_size * 100
    print("\nSize of df after removing rows based on duration:", after_duration_size, file=sys.stdout)
    print("Reduction percentage after removing rows based on duration:", reduction_percentage_duration, file=sys.stdout)

    #  remove basd on ratio of time from v1 to peak and peak to v2
            
    # Remove based on tan ( angles between valleys and peak | how sharp the eiid is )
    
    
    tv1=df['dur from v1 to peak']
    tv2=df['dur from start v1 to v2']- tv1
    ratio= tv1/tv2
    
    
            
    tanv1= (df['peak_ampl'] + abs(df['start_val_ampl'])) / tv1
    tanv2= (df['peak_ampl'] + abs(df['end_val_ampl'])) / tv2
    
    df['tanv1']= tanv1
    df['tanv2']=tanv2
    
    df['ratio'] = ratio
    
    #mask= ( df['ratio']  > 1.6) | (df['ratio'] < 0.35) | (df['tanv1'] < 400) | (df['tanv1'] >3000) |  (df['tanv2']<350) | ( df['tanv2']> 1000 )  
    mask= ( df['ratio']  > 1.6 )| (df['ratio'] < 0.35) | (df['tanv1'] < 400)| (df['tanv1'] >4000) |  (df['tanv2']<250) | ( df['tanv2']> 1500 )
    df = df[~mask]
    
    # Reset the index of the filtered DataFrame
    df.reset_index(drop=True, inplace=True)





    after_val_duration_size = len(df)
    reduction_percentage_duration = (after_duration_size - after_val_duration_size) / after_peak_size * 100
    print("\nSize of df after removing rows based on  valleys to peak duration ratio and angles:", after_duration_size, file=sys.stdout)
    print("Reduction percentage after removing rows based on valleys to peak duration  ratio and angles:", reduction_percentage_duration, file=sys.stdout)
    

    

    

 
    
    
    
    final_size = len(df)
    print("\n\nInitial size of df:", initial_size, file=sys.stdout)
    print("Final size of df:", final_size, file=sys.stdout)
    reduction_percentage = (initial_size - final_size) / initial_size * 100
    print("Reduction percentage after all cleaning:", reduction_percentage, file=sys.stdout)
    
    return df, initial_indexes