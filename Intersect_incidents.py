# Here we are looking for intersection between point (incidents) and poligons 
# (area, which is zip-codes)

#Note: the process of looking for intersection is based on shapefile. 
# For this reason a shapefile with zipcodes where donwladed from:
# https://data.austintexas.gov/Locations-and-Maps/Zipcodes/ghsj-v65t 
# The file can be access here:
# https://data.austintexas.gov/api/geospatial/ghsj-v65t?method=export&format=Shapefile

#path_zipcodes: path to the file with zipcodes 
def intersect(df, path_zipcodes):

    # Import libraries:
    # PART A: Converte csv file into shapefile
    from geopandas import GeoDataFrame
    from shapely.geometry import Point
    
    # PART B: Find intersection between shapefiles
    import geopandas as gpd
    import os
    
    zipcodes='zips.shp'
    

    # PART A
    #Filter data 
    df=df[['Issue Reported','Latitude','Longitude']]
    
    #Convert points (csv file) into shapefile (just changin format)
    geometry = [Point(xy) for xy in zip(df.Longitude, df.Latitude)]
    #df = df.drop(['Longitude', 'Latitude'], axis=1)
    crs = {'init': 'epsg:4326'}
    gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
    
    
    # PART B
    #Find intersection between points (accidents) and poligons (zipcodes)
    gdfLeft = gpd.read_file(os.path.join(path_zipcodes,zipcodes))
    gdfRight = gdf
    
    gdfJoined = gpd.sjoin(gdfLeft, gdfRight, how="left", op='intersects')
    
    
    ## CHECK (uncommend if needed)
    # In order to check if process went correct. Below code was used. 
    # Random sample of 2000 points were chosen, save into csv file and 
    # plotted in QGIS software and compared with zipcodes.
    '''test_random=gdfJoined.sample(2000) 
    test_random.to_csv(path+'random.csv',sep=',')'''
    
    
    # Select columns
    Incidents=gdfJoined[['zipcode','Issue Reported']]
    
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
        print("WARNING: categories have changed. Please check the code to group a new category.")
    
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
    
    return Incidents