################# Functions descriptions #################
##########################################################
# Here we are looking for intersection between point (incidents) and poligons 
# (area, which is zip-codes)
# Note: the process of looking for intersection is based on shapefile. 
# For this reason a shapefile with zipcodes where donwladed from:
# https://data.austintexas.gov/Locations-and-Maps/Zipcodes/ghsj-v65t 
# The file can be access here:
# https://data.austintexas.gov/api/geospatial/ghsj-v65t?method=export&format=Shapefile
# What function does is: 
# a) transform a csv file (number 5 accidents) which contains Longitude and Latitude 
#    of every single accident in Austin into poligon object (so the intersection
#    later can be found easier).
# b) read a poligon (shapefile) with zip-codes from the file.
# c) Intersect two poligons
# d) as a result we assign to every accident a zip-code, where the accident
#    occured. Rest of the work is done in the Function 4. Where accidents are
#    grouped.


#################################### Imports #################################
import warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.INFO)
logging=logging.getLogger()


# PART I: Converte csv file into shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point
    
# PART II: Find intersection between shapefiles
import geopandas as gpd
import os



############################ Function 3 #######################################       
def intersect(df, path_zipcodes):
    logging.info("Now CSV 5, we need to intersect accidents with zip-codes")
    
    
    #PART I
    #path_zipcodes: path to the file with zipcodes 
    zipcodes='zips.shp'

    #Filter data 
    df=df[['Issue Reported','Latitude','Longitude']]
    
    #Convert points (csv file) into shapefile (just changin format)
    geometry = [Point(xy) for xy in zip(df.Longitude, df.Latitude)]
    #df = df.drop(['Longitude', 'Latitude'], axis=1)
    crs = {'init': 'epsg:4326'}
    gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
    
    
    # PART II
    #Find intersection between points (accidents) and poligons (zipcodes)
    gdfLeft = gpd.read_file(os.path.join(path_zipcodes,zipcodes))
    gdfRight = gdf
    #Join the data
    gdfJoined = gpd.sjoin(gdfLeft, gdfRight, how="left", op='intersects')
    
    
    # PART III
    ## CHECK (uncommend if needed)
    # In order to check if process went correct. Below code was used. 
    # Random sample of 2000 points were chosen, save into csv file and 
    # plotted in QGIS software and compared with zipcodes.
    '''test_random=gdfJoined.sample(2000) 
    test_random.to_csv(path+'random.csv',sep=',')'''
    
    
    # PART IV
    # Select what columns needed
    Incidents=gdfJoined[['zipcode','Issue Reported']]
    
    logging.info("Intersection succes!")
    
    return Incidents