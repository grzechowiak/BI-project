# Project

########################################
########## Imports ##################### 
import pandas as pd

########################################
########## Getting the data ############
links = ['https://data.austintexas.gov/api/views/hcnj-rei3/rows.csv',
         'https://data.austintexas.gov/api/views/sxk7-7k6z/rows.csv',
         'https://data.austintexas.gov/api/views/ecmv-9xxi/rows.csv',
         'https://data.austintexas.gov/api/views/dx9v-zd7x/rows.csv',
         'https://data.austintexas.gov/api/views/b4k4-adkb/rows.csv',
         'https://data.austintexas.gov/resource/sxk7-7k6z.csv',
         'https://data.austintexas.gov/resource/x9yh-78fz.csv',
         'https://data.texas.gov/resource/naix-2893.csv']

######## DATA FROM THE USA GOVERNMENT ########
#### 2014 Housing Market Analysis Data by Zip Code #### 
df1 = pd.read_csv(links[0])

#### Austin Water - Residential Water Consumption ####
df2 = pd.read_csv(links[1])  

#### Food Establishment Inspection Scores ####
df3 = pd.read_csv(links[2])

#### Real-Time Traffic Incident Reports ####
df4 = pd.read_csv(links[3])

#### Traffic Cameras #### 
df5 = pd.read_csv(links[4])

######## DATA FROM AUSTIN TEXAS LOCAL GOVERNMENT ########
#### Commercial Water Consumption ####
df6 = pd.read_csv(links[5])

#### Issued Construction Permits (FILE 433MB) ####
#Link to data: https://data.austintexas.gov/Building-and-Development/Issued-Construction-Permits/3syk-w9eu
df7 = pd.read_csv(links[6])

######## DATA FROM TEXAS GOVERNMENT ########
####Mixed Beverage Gross Reciepts ####
#Link to data: https://data.texas.gov/Government-and-Taxes/Mixed-Beverage-Gross-Receipts/naix-2893
df8 = pd.read_csv(links[7])


########################################
########## Choosing columns ############

df8.head()
len(df8.columns)




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
pd.merge(df1_2, df3, how='right', left_on=['Zip Code'], right_on=['Postal Code'])
