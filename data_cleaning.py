import logging

logging.basicConfig(level=logging.INFO)
logging=logging.getLogger()

def clean_data(df1,df2,df3,df4):

    logging.info("Let's do some cleaning")
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
    logging.info("CSV 1 is cleaned")
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
   
    logging.info("CSV 2 is cleaned")
    #DF3
    #### Food Establishment Inspection Scores ####
    df3.head()
    df3.columns
    #Check NAs
    df3.count() #no missing values
    #group by Zip Code, and take the median of Score
    df3 = df3.groupby('Zip Code').median().reset_index()
    
    logging.info("CSV 3 is cleaned")
    #DF4
    ####Mixed Beverage Gross Reciepts ####
    #Select only city Austin
    df4 = df4[df4['location_city']=='AUSTIN']
    df4.drop('location_city', axis=1,inplace=True)
    df4 = df4.groupby('location_zip').sum().reset_index()

    df4.count() #no missing values
    
    logging.info("CSV 4 is cleaned")
    
    return (df1,df2,df3,df4)


def clean_df5(Incidents):
    logging.info("Now, we clean CSV5")
    # Group by (zipcode and type of incident). 
    # Take the count of how many incidents for each zipcode are for each type
    Incidents=Incidents.groupby(['zipcode','Issue Reported']).size().reset_index()
    Incidents.rename(columns={0:'Total incidents'}, inplace=True)
    Incidents = Incidents.pivot('zipcode', 'Issue Reported', 'Total incidents').reset_index()
    #create new columns, which are summation for each general category
    #CATEGORIES:
        # FATAL/INJURY_ACC -> 'FLEET ACC/ FATAL', 'TRAFFIC FATALITY', 'COLLISION WITH INJURY', 'Crash Urgent', 'FLEET ACC/ INJURY'
        # COLLISION_ACC -> 'COLLISION', 'COLLISION/PRIVATE PROPERTY', 'COLLISN / FTSRA','COLLISN/ LVNG SCN', 'AUTO/ PED'
        # OTHER_ACC -> 'BOAT ACCIDENT', 'LOOSE LIVESTOCK', 'N / HZRD TRFC VIOL',  'HIGH WATER', 'ICY ROADWAY'
        # CAR/TRAFFIC_ACC -> 'TRFC HAZD/ DEBRIS', 'VEHICLE FIRE', 'Crash Service', 'Traffic Hazard', 'Traffic Impediment','zSTALLED VEHICLE', 'BLOCKED DRIV/ HWY'
    
    #check categories
    categories = ['AUTO/ PED', 'BLOCKED DRIV/ HWY', 'BOAT ACCIDENT', 'COLLISION',
       'COLLISION WITH INJURY', 'COLLISION/PRIVATE PROPERTY',
       'COLLISN / FTSRA', 'COLLISN/ LVNG SCN', 'Crash Service', 'Crash Urgent',
       'FLEET ACC/ FATAL', 'FLEET ACC/ INJURY', 'HIGH WATER', 'ICY ROADWAY',
       'LOOSE LIVESTOCK', 'N / HZRD TRFC VIOL', 'TRAFFIC FATALITY',
       'TRFC HAZD/ DEBRIS', 'Traffic Hazard', 'Traffic Impediment',
       'VEHICLE FIRE', 'zSTALLED VEHICLE']
    
    #check if a category was added at the Austin website
    check = Incidents.columns.all() in categories
    if not check:
        logging.warning("categories have changed. Please check the code to group a new category.")
    
    Incidents.loc[:,'AUTO/ PED':'zSTALLED VEHICLE'] = Incidents.loc[:,'AUTO/ PED':'zSTALLED VEHICLE'].fillna(0)
    
    #create FATAL/INJURY_ACC column and drop the smaller categories
    Incidents['FATAL/INJURY_ACC'] = Incidents['FLEET ACC/ FATAL'] + Incidents['TRAFFIC FATALITY']
    Incidents['COLLISION WITH INJURY'] + Incidents['Crash Urgent'] + Incidents['FLEET ACC/ INJURY']
    Incidents.drop(['FLEET ACC/ FATAL', 'TRAFFIC FATALITY', 'COLLISION WITH INJURY', 
                    'Crash Urgent', 'FLEET ACC/ INJURY'], axis=1, inplace=True)
    
    #create COLLISION_ACC column and drop the smaller categories
    Incidents['COLLISION_ACC'] = Incidents['COLLISION'] + Incidents['COLLISION/PRIVATE PROPERTY'] 
    + Incidents['COLLISN / FTSRA'] + Incidents['COLLISN/ LVNG SCN'] + Incidents['AUTO/ PED']
    Incidents.drop(['COLLISION', 'COLLISION/PRIVATE PROPERTY', 'COLLISN / FTSRA',
                    'COLLISN/ LVNG SCN', 'AUTO/ PED'], axis=1, inplace=True)
    
    #create OTHER_ACC column and drop the smaller categories
    Incidents['OTHER_ACC'] = Incidents['BOAT ACCIDENT'] + Incidents['LOOSE LIVESTOCK'] 
    + Incidents['N / HZRD TRFC VIOL'] + Incidents['HIGH WATER'] + Incidents['ICY ROADWAY']
    Incidents.drop(['BOAT ACCIDENT', 'LOOSE LIVESTOCK', 'N / HZRD TRFC VIOL',
                    'HIGH WATER', 'ICY ROADWAY'],axis=1, inplace=True)
    
    #create CAR/TRAFFIC_ACC column and drop the smaller categories
    Incidents['CAR/TRAFFIC_ACC'] = Incidents['TRFC HAZD/ DEBRIS'] + Incidents['VEHICLE FIRE'] 
    + Incidents['Crash Service'] + Incidents['Traffic Hazard'] + Incidents['Traffic Impediment'] 
    + Incidents['zSTALLED VEHICLE'] + Incidents['BLOCKED DRIV/ HWY']
    Incidents.drop(['TRFC HAZD/ DEBRIS', 'VEHICLE FIRE', 'Crash Service', 'Traffic Hazard', 'Traffic Impediment','zSTALLED VEHICLE', 'BLOCKED DRIV/ HWY'], axis=1, inplace=True)
    
    #get rid of name='Issue Reported'
    Incidents = Incidents.rename_axis(None, axis=1).reset_index()
    Incidents['zipcode'] = Incidents['zipcode'].astype(int)
    
    logging.info("CSV 5 cleaned!")
    return Incidents


def fill_nas(data):
    logging.info("Dealing with NA values")
    data.loc[:,'beer_receipts':'CAR/TRAFFIC_ACC'] = data.loc[:,'beer_receipts':'CAR/TRAFFIC_ACC'].fillna(0)
    logging.info("NA vales filled by zeros!")
    
    return data
    
def check_nas(data):
    logging.info("Let's check if there are any column with NA values")
    missing_data = data.isnull() #localize NULLs
    missing_data.head(5)
    # Go thru missing_data and print if TURE
    print("Missing values were found in columns:\n")
    for column in missing_data.columns.values.tolist():
        if True in missing_data[column].values:
            print(column)
            print(missing_data[column].value_counts())
            print("")