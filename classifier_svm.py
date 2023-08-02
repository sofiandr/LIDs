# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 18:46:54 2023


  FEED THE SVM AND CLEANING FURTHER 
  
  svm trained model needs to saved somewhere in the path
 
@author: SOFIA
"""

import scipy 
import sys
def classifier_svm(j,df,iids,iidsFiltered,model_path):

       
        
        # import svm model i trained
        
        import joblib

        model = joblib.load(model_path)
        
        # feed with iids
        
        predictions = model.predict(iids)
        
        filtered_indexes = [i for i, prediction in enumerate(predictions) if prediction == 1]
        iids_ML = [iids[i] for i in filtered_indexes]
        iidsFiltered_ML = [iidsFiltered[i] for i in filtered_indexes]
        

        scipy.io.savemat("eIIDs_ch" + str(j) +
                         "_ML.mat", mdict={'eiids_ML': iids_ML})
        print('Saved .mat files')
        print('Size after ML:', len(iids_ML), file=sys.stdout )
        scipy.io.savemat("eIIDsFiltered_ch" + str(j) +
                         "_ML.mat", mdict={'eiidsFilt_ML': iidsFiltered_ML})



        
        # Create a new DataFrame 'df_ML' using the filtered indexes
        df_ML = df.loc[filtered_indexes]

        # Save 'df_ML' as CSV
        df_ML.to_csv("eIIDss_char_ch" + str(j) + "_ML.csv", index=False)

        print('Saved df_ML as CSV')    
        
        



