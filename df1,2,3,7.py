

#DF 1: 
#### 2014 Housing Market Analysis Data by Zip Code #### 

df1=df1[['Zip Code','Median household income','Non-White, Non-Hispanic or Latino', 'Hispanic or Latino, of any race',
         'Unemployment','Median rent','Median home value','Average monthly transportation cost']]

#Unfortunately, one zip-code is missing. Drop this row.
df1.count()

#Zip Code has NA, delete NA only if NA is found in column Zip Code
df1.dropna(subset=['Zip Code'], inplace = True)
# Change data type 
df1["Zip Code"] = df1["Zip Code"].astype(int)
df1.dtypes

#DF 2:
#### Austin Water - Residential Water Consumption ####
df2.head()
#Check NA values
df2.count() #No missing values


#DF3
#### Food Establishment Inspection Scores ####
df3.head()
df3.columns
#Check NAs
df3.count() #no missing values


#DF7
####Mixed Beverage Gross Reciepts ####
df7.columns
#Select only city Austin
df7=df7[df7['location_city']=='AUSTIN']
df7.groupby('location_zip').size()
#test file to see
#df7.to_csv('C:\\Users\\grzechu\\Desktop\\TTU\\ProjectsSpringGIT\\BI_Project\\BI-project\\zip.csv')
df7=df7[['beer_receipts','liquor_receipts','location_zip','wine_receipts','total_receipts']]
## what is it : cover_charge_receipts?
df7.count() #no missing values



#MERGE df1 + df2
#Merge right join. We want everything from df2 and join to it df1
df1_2=pd.merge(df1, df2, how='right', left_on=['Zip Code'], right_on=['Postal Code'])
df1_2.count()
#We don't need column "Zip Code" from column, we're gonna use Postal Code from df2 
df1_2=df1_2.drop(columns=["Zip Code"])
len(df1_2.columns) # Check