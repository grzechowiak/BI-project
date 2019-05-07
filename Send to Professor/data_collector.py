################# Functions descriptions #################
##########################################################
## This file contains functions number 1 and 5(find the order in main())
## 1. import_process_data -> download all five files (df1,df2,df3,df4,df5)
## 5. merge_data -> merge all data together (df1,df2,df3,df4,df5 into one final file)

#################################### Imports #################################
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.INFO)
logging=logging.getLogger()

############################### Function 1 ###################################
def import_process_data():
    #Specify all links
    links = ['https://data.austintexas.gov/api/views/hcnj-rei3/rows.csv',
             'https://data.austintexas.gov/api/views/sxk7-7k6z/rows.csv',
             'https://data.austintexas.gov/api/views/ecmv-9xxi/rows.csv',
             'https://data.texas.gov/resource/naix-2893.csv',
             'https://data.austintexas.gov/api/views/dx9v-zd7x/rows.csv']
    
    ############### Start collecting the files ###############
    
    ######## DATA FROM THE USA GOVERNMENT ########
    ####df1: 2014 Housing Market Analysis Data by Zip Code #### 
    logging.info("Please wait, we are downloading CSV1")
    df1 = pd.read_csv(links[0]) 
    logging.info("Ok, CSV 1 loaded")
    
    ####df2: Austin Water - Residential Water Consumption ####
    logging.info("Please wait, we are downloading CSV2")
    df2 = pd.read_csv(links[1])
    logging.info("OK, CSV 2 loaded")
    
    ####df3: Food Establishment Inspection Scores ####
    logging.info("Please wait, we are downloading CSV3")
    df3 = pd.read_csv(links[2], usecols=['Zip Code', 'Score']) 
    logging.info("Ok, CSV 3 loaded")
    
    ######## DATA FROM TEXAS GOVERNMENT #######
    ####df4: Mixed Beverage Gross Reciepts ####
    #Link to data: https://data.texas.gov/Government-and-Taxes/Mixed-Beverage-Gross-Receipts/naix-2893
    df4 = pd.read_csv(links[3], usecols=['location_city', 'beer_receipts',
                      'liquor_receipts','location_zip','wine_receipts','total_receipts']) 
    #The df4 is for all Texas, so later it has to be filtered by location for Austin.
    #We don't download all files, mostly in order to shorten the time. 
    logging.info("Please wait, we are downloading CSV4")
    logging.info("Ok, CSV 4 loaded")
    
    #####df5: Real-Time Traffic Incident Reports ####
    logging.info("Please wait, we are downloading CSV5")
    df5 = pd.read_csv(links[4], usecols=['Issue Reported', 'Latitude', 'Longitude'])
    #We download only 3 columns from the file. The most important is location
    #latitude and longitude
    logging.info("Ok, CSV 5 loaded")
    return (df1,df2,df3,df4,df5)


############################### Function 5 ###################################
def merge_data(df1,df2,df3,df4, df5):    
    logging.info("Merging CSV1, CSV2, CSV3, CSV4, CSV5 together")
    
    ### MERGE df1 + df2 ###
    #Merge right join. We want everything from df2 and join to it df1
    df_merged=pd.merge(df1, df2, how='right', left_on=['Zip Code'], right_on=['Postal Code'])
    df_merged.count()
    #We don't need column "Zip Code" from column, we're gonna use Postal Code from df2 
    df_merged=df_merged.drop(columns=["Zip Code"])
    logging.info("Merged 1 and 2")
    
    ###MERGE (df1 + df2) + df3 ###
    #Merge right join. We want everything from df_merged and join to it df3
    df_merged = pd.merge(df_merged, df3, how='right', left_on=['Postal Code'], right_on=['Zip Code'])
    df_merged=df_merged.drop(columns=["Postal Code"])
    logging.info("Merged 1,2 and 3")

    ###MERGE (df1 + df2+ df3) + df4 ###
    #Merge right join. We want everything from df_merged and join to it df4
    df_merged = pd.merge(df4, df_merged, how='right', left_on=['location_zip'], right_on=['Zip Code'])
    df_merged=df_merged.drop(columns=["location_zip"])
    logging.info("Merged 1,2,3 and 4")
    
    ###MERGE (df1 + df2+ df3+ df4) + df5 ###
    #Merge right join. We want everything from df5 and join to it df_merged
    df_merged = pd.merge(df_merged, df5, how='right', left_on=['Zip Code'], right_on=['zipcode'])
    df_merged=df_merged.drop(columns=["Zip Code"])
    logging.info("Merged 1,2,4 and 5")
    
    logging.info("All merged!")

    
    return df_merged