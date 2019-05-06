################# Functions descriptions #################
##########################################################
#the main() call all the functions necessary in the projetct. 


###################################### Imports ###############################
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
    
############################### User inputs ##################################
# We need a file with Zipcodes (shapefile in folder Files\\Zipcodes) in order
# to intersect accidents with poligons containing Zipcodes. This files is not
# available to download easily by link so it has to be loaded by hand.
    print('##########################################################')    
    print(' ')   
    print('There are some warnings. No need to worry about them! :)')
    print('### ############ ###') 
    print('### INSTRUCTIONS ###') 
    print('### ############ ###') 
    print('The code needs following libraries to be installed: pandas, geopandas, shapely and rtree')
    print('You are asked for two paths to input and the whole process will start.')
    print('(1):The first path you need to localize the folder with the file called: zips.shp')
    print('Example would be: C:\\Users\\users_name\\BI_Project\\files\\Zipcodes')   
    path_zip=input('Enter the (1) First path: ')
    print(' ') 
# User input, where you want to store your final merged, cleaned file.   
    print('(2): The second path is where you want to save output file.')
    output= input('Enter the (2) Second path: ')
    try:
##################### Function 1: from data_collector ########################
        # Import (df1 to df5) from Austin Gov. website
        (df1,df2,df3,df4,df5)=import_process_data()
        
##################### Function 2: from data_cleaning #########################
        #Clean df1 to df4
        (df1,df2,df3,df4)=clean_data(df1,df2,df3,df4)
        
##################### Function 3: from Intersect_incidents ###################       
        # Find intersection between accidents and zipcodes
        df5 = intersect(df5, path_zip)
        
##################### Function 4: from data_cleaning #########################        
        #Clean df5
        df5=clean_df5(df5)
    
##################### Function 5: from data_collector ########################        
        #Merge df1 to df5
        final_df=merge_data(df1,df2,df3,df4, df5)
        
##################### Function 6: from data_cleaning #########################        
        # Fill all na values in merged data frame
        final_df=fill_nas(final_df)

##################### Function 7: from data_cleaning #########################        
        # Check all NAs values in merged data set
        check_nas(final_df)
        
##################### Save the data into .csv file ###########################        
        final_df.to_csv(output + 'final_data.csv')
        #just a logg to display for user.
        logging.info("Done! Your file is ready and saved in your output!")
        
##################### If any error spotted, print it for user ################        
    except Exception as err:
        logging.error("error is:",err)
    # just an input to not close the console automatically    
    input("Press enter to exit :)")

########################### Call the main Function ###########################        
main()