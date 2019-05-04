from data_collector import merge_data
from data_collector import import_process_data

from data_cleaning import clean_data
from data_cleaning import clean_df5
from data_cleaning import fill_nas
from data_cleaning import check_nas

from Intersect_incidents import intersect

import warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.INFO)
logging=logging.getLogger()



def main():
    path_zip=input('Enter the path to the folder called Zipcodes (inside folder: files): ')
    output= input('Enter where you wanna save a new file: ')

    try:
        # Import (df1 to df5) from Austin Gov. website
        (df1,df2,df3,df4,df5)=import_process_data()
        
        #Clean df1 to df4
        (df1,df2,df3,df4)=clean_data(df1,df2,df3,df4)
        
        # Find intersection between accidents and zipcodes
        df5 = intersect(df5, path_zip)
        
        #Clean df5
        df5=clean_df5(df5)
    
        #Merge df1 to df5
        final_df=merge_data(df1,df2,df3,df4, df5)
        
        # Fill all na values in merged data frame
        final_df=fill_nas(final_df)
        
        # Check all NAs values in merged data set
        check_nas(final_df)
        
        #Save the data
        final_df.to_csv(output + 'final_data.csv')
        logging.info("Done! Your file is ready and saved in your output!")
        
    ##Check the error, in any    
    except Exception as err:
        logging.error("error is:",err)
    input("Press enter to exit :)")
main()