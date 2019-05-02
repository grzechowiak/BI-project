

def clean_data(df1,df2,df3,df4):


    #DF 1: 
    #### 2014 Housing Market Analysis Data by Zip Code #### 
    #Unfortunately, one zip-code is missing. Drop this row.
    df1.count()
    #Zip Code has NA, delete NA only if NA is found in column Zip Code
    df1.dropna(subset=['Zip Code'], inplace = True)
    # Change data type 
    df1["Zip Code"] = df1["Zip Code"].astype(int)
    df1.dtypes
    # After droping one Zipcode, some other columns have NA's
    # we don't want to delete them so we input zero in NA
    df1[df1['Homes affordable to people earning less than $50,000'].isnull()]
    df1['Homes affordable to people earning less than $50,000'].fillna(0, inplace=True)
    
    df1[df1['Owner units affordable to average retail/service worker'].isnull()]
    df1['Owner units affordable to average retail/service worker'].fillna(0, inplace=True)
    
    df1[df1['Owner units affordable to average teacher'].isnull()]
    df1['Owner units affordable to average teacher'].fillna(0, inplace=True)
    
    df1[df1['Owner units affordable to average tech worker'].isnull()]
    df1['Owner units affordable to average tech worker'].fillna(0, inplace=True)
    
    df1[df1['Owner units affordable to average artist'].isnull()]
    df1['Owner units affordable to average artist'].fillna(0, inplace=True)
    
    df1.count()
    #No more missing values in df1
    
    #DF 2:
    #### Austin Water - Residential Water Consumption ####
    df2.head()
    #Check NA values
    df2.count() #No missing values
    df2 = df2[['Postal Code','Customer Class', 'Total Gallons']]
    #group by (Postal Code, Customer Class) -> create new column sum of Total Gallons for each class
    df2_group = df2.groupby(['Postal Code','Customer Class'], as_index=False).sum()
    #transpose from rows to columns the total gallons per category
    df2 = df2_group.reset_index().pivot('Postal Code', 'Customer Class', 'Total Gallons')
    #change names of columns 
    df2.rename(columns={'Irrigation - Multi-Family':'I-MF-Tot.Gallons', 
                        'Irrigation - Residential':'I-R-Tot.Gallons',
                        'Multi-Family':'MF-Tot.Gallons', 'Residential':'R-Tot.Gallons'}, inplace=True)
    
    #get rid of name='Customer Class'
    df2 = df2.rename_axis(None, axis=1).reset_index()
    #replace all NA values by 0 for all the columns. 
    #It might happen that a zip code does not have a particular type of Customer Class, so it does not
    # make sense taking other policies such as median or mean.
    df2.loc[:,'I-MF-Tot.Gallons':'R-Tot.Gallons'] = df2.loc[:,'I-MF-Tot.Gallons':'R-Tot.Gallons'].fillna(0)
   
    #DF3
    #### Food Establishment Inspection Scores ####
    df3.head()
    df3.columns
    #Check NAs
    df3.count() #no missing values
    #group by Zip Code, and take the median of Score
    df3 = df3.groupby('Zip Code').median().reset_index()
    
    
    #DF5
    ####Mixed Beverage Gross Reciepts ####
    #Select only city Austin
    df4 = df4[df4['location_city']=='AUSTIN']
    df4.drop('location_city', axis=1,inplace=True)
    df4 = df4.groupby('location_zip').sum().reset_index()

    df4.count() #no missing values
    
    return (df1,df2,df3,df4)