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
         'https://data.austintexas.gov/resource/d9pb-3vh7.csv',
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

#### Residential Average Monthly kWh and Bills ####
#Link to data: https://data.austintexas.gov/Utilities-and-City-Services/Residential-Average-Monthly-kWh-and-Bills/d9pb-3vh7
df8 = pd.read_csv(links[7])

######## DATA FROM TEXAS GOVERNMENT ########
####Mixed Beverage Gross Reciepts ####
#Link to data: https://data.texas.gov/Government-and-Taxes/Mixed-Beverage-Gross-Receipts/naix-2893
df9 = pd.read_csv(links[8])



from uszipcode import SearchEngine

def getzipcode(row):   
    search = SearchEngine(simple_zipcode=False)
    result = search.by_coordinates(row['Latitude'],row['Longitude'], radius=30)
    
    
    zipcodes = []
    for x in result:
        zipcodes.append((x.zipcode,x.radius_in_miles))
    
    zipcodes.sort(key=lambda x: x[1])
    if len(zipcodes) == 0:
        return -1
    else:
        return zipcodes[0][0]


df4['ZipCode'] = df4.apply(getzipcode, axis = 1)
df4['Latitude'][0].dtype
    
    
    
    
    
    
    
    
    
    
    
