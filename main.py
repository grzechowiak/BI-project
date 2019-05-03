from data_collector import check_fix_na
from data_collector import merge_data
from data_collector import import_process_data

from data_cleaning import clean_data
from data_cleaning import clean_df5

from Intersect_incidents import intersect

import logging

logging.basicConfig(level=logging.INFO)
logging=logging.getLogger()

def main():
    path_zip=input('Enter the path to the folder called Zipcodes (inside folder: files): ')
    #'C:\\Users\\grzechu\\Desktop\\TTU\\ProjectsSpringGIT\\BI_Project\\BI-project\\files\\Zipcodes\\zips.shp'
    #input('Enter the path to the folder called Zipcodes (inside folder: files): ')
    output= input('Enter where you wanna save a new file: ')
    #'C:\\Users\\grzechu\\Desktop\\TTU\\ProjectsSpringGIT\\BI_Project\\'
   # input('Enter where you wanna save a new file: ')
    
    
    
    (df1,df2,df3,df4,df5)=import_process_data()
    
    (df1,df2,df3,df4)=clean_data(df1,df2,df3,df4)
    
        ## A FUNCTION ##
    #get grouped incidents data by zipcodes
    df5 = intersect(df5, path_zip)
    logging.info("loaded 5 intersected")
    
    df5=clean_df5(df5)
    logging.info("loaded 5 intersected, cleaned")

    
    final_df=merge_data(df1,df2,df3,df4, df5)
    logging.info("finish merging")
    
    final_df=check_fix_na(final_df)
    
    
    
    #Save the data
    print(final_df.head())
    final_df.to_csv(output + 'final_data.csv')
    
    input("Press enter to exit ;)")

main()
