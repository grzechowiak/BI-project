# Project

########################################
########## Imports ##################### 
import pandas as pd
from Intersect_incidents import intersect
from data_cleaning import clean_data



def import_data(path_zipcodes):
    ########################################
    ########## Getting real time data ############
    links = ['https://data.austintexas.gov/api/views/hcnj-rei3/rows.csv',
             'https://data.austintexas.gov/api/views/sxk7-7k6z/rows.csv',
             'https://data.austintexas.gov/api/views/ecmv-9xxi/rows.csv',
             'https://data.texas.gov/resource/naix-2893.csv',
             'https://data.austintexas.gov/api/views/dx9v-zd7x/rows.csv']
    
    ######## DATA FROM THE USA GOVERNMENT ########
    #### 2014 Housing Market Analysis Data by Zip Code #### 
    df1 = pd.read_csv(links[0]) 
    
    #### Austin Water - Residential Water Consumption ####
    df2 = pd.read_csv(links[1])
    
    #### Food Establishment Inspection Scores ####
    df3 = pd.read_csv(links[2], usecols=['Zip Code', 'Score']) 
    
    
    ######## DATA FROM TEXAS GOVERNMENT ########
    ####Mixed Beverage Gross Reciepts ####
    #Link to data: https://data.texas.gov/Government-and-Taxes/Mixed-Beverage-Gross-Receipts/naix-2893
    df4 = pd.read_csv(links[3], usecols=['location_city', 'beer_receipts','liquor_receipts','location_zip','wine_receipts','total_receipts']) 
    #Filter by location_city cuz it's for all Texas
    #keep: beer_receipts,liquor_receipts,location_city,location_zip,
    #total_receipts,wine_receipts group by zipcode and take totals 
    
    
    (df1,df2,df3,df4) = clean_data(df1,df2,df3,df4)
    
    #### Real-Time Traffic Incident Reports ####
    df5 = pd.read_csv(links[4], usecols=['Issue Reported', 'Latitude', 'Longitude']) 
    
    #get grouped incidents data by zipcodes
    path_zipcodes = "/Users/mikaelapisanileal/Documents/BI-project/files/Zipcodes/"
    df5 = intersect(df5, path_zipcodes)
    
    return (df1,df2,df3,df4,df5)
    
def check_fix_na(data):
    missing_data = data.isnull() #localize NULLs
    missing_data.head(5)
    # Go thru missing_data and print if TURE
    print("Missing values were found in columns:\n")
    for column in missing_data.columns.values.tolist():
        if True in missing_data[column].values:
            print(column)
            print(missing_data[column].value_counts())
            print("")
    data.loc[:,'beer_receipts':'CAR/TRAFFIC_ACC'] = data.loc[:,'beer_receipts':'CAR/TRAFFIC_ACC'].fillna(0)
    return data


def merge_data(df1,df2,df3,df4, df5):    
    
    #MERGE df1 + df2
    #Merge right join. We want everything from df2 and join to it df1
    df_merged=pd.merge(df1, df2, how='right', left_on=['Zip Code'], right_on=['Postal Code'])
    df_merged.count()
    #We don't need column "Zip Code" from column, we're gonna use Postal Code from df2 
    df_merged=df_merged.drop(columns=["Zip Code"])
    
    #MERGE df1 + df2 + df3
    #Merge right join. We want everything from df_merged and join to it df3
    df_merged = pd.merge(df_merged, df3, how='right', left_on=['Postal Code'], right_on=['Zip Code'])
    df_merged=df_merged.drop(columns=["Postal Code"])

    df_merged = pd.merge(df4, df_merged, how='right', left_on=['location_zip'], right_on=['Zip Code'])
    df_merged=df_merged.drop(columns=["location_zip"])
    
    df_merged = pd.merge(df_merged, df5, how='right', left_on=['Zip Code'], right_on=['zipcode'])
    df_merged=df_merged.drop(columns=["Zip Code"])
    
    df_merged = check_fix_na(df_merged)
    
    return df_merged

    
