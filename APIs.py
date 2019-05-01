# Project

########################################
########## Imports ##################### 
import pandas as pd
from Intersect_incidents import intersect
from data_cleaning import clean_data

########################################
########## Getting the data ############
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


dfs = clean_data(df1,df2,df3,df4)

#### Real-Time Traffic Incident Reports ####
df5 = pd.read_csv(links[4], usecols=['Issue Reported', 'Latitude', 'Longitude']) 
#get grouped incidents data by zipcodes
incidents_grouped = intersect(df5)


##############################################################################
############################ OLD MERGING CODE #######################################
#############################################################################


########################################
########## Merging ##################### 
#DF1
df1.head()
#Check NA values
df1.count()
#Zip Code has NA, delete NA only if NA is found in column Zip Code
df1.dropna(subset=['Zip Code'], inplace = True)
# Change data type 
df1["Zip Code"] = df1["Zip Code"].astype(int)
df1.dtypes

#DF2
df2.head()
#Check NA values
df2.count()

#MERGE df1 + df2
#Merge right join. We want everything from df2 and join to it df1
df1_2=pd.merge(df1, df2, how='right', left_on=['Zip Code'], right_on=['Postal Code'])
df1_2.count()
#We don't need column "Zip Code" from column, we're gonna use Postal Code from df2 
df1_2=df1_2.drop(columns=["Zip Code"])
len(df1_2.columns) # Check


#DF3
df3.head()
df3.columns
#Check NAs
df3.count() #Wow, no NA's

#MERGE df1 + df2
#Merge right join. We want everything from df2 and join to it df1
df_merged = pd.merge(df1_2, df3, how='right', left_on=['Zip Code'], right_on=['Postal Code'])


