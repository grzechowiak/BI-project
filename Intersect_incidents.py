# Here we are looking for intersection between point (incidents) and poligons 
# (area, which is zip-codes)

#Note: the process of looking for intersection is based on shapefile. 
# For this reason a shapefile with zipcodes where donwladed from:
# https://data.austintexas.gov/Locations-and-Maps/Zipcodes/ghsj-v65t 
# The file can be access here:
# https://data.austintexas.gov/api/geospatial/ghsj-v65t?method=export&format=Shapefile

def intersect():
# Import libraries:
# PART A: Converte csv file into shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

# PART B: Find intersection between shapefiles
import geopandas as gpd
import os

#Shapefile with zipcodes were downloaded and read from local computer:
path='C:\\Users\\grzechu\\Desktop\\TTU\\ProjectsSpringGIT\\BI_Project\\BI-project\\files\\Zipcodes\\'
zipcodes='zips.shp'



# PART A
#Filter data 
df=df4[['Issue Reported','Location','Latitude','Longitude']]

#Convert points (csv file) into shapefile (just changin format)
geometry = [Point(xy) for xy in zip(df.Longitude, df.Latitude)]
#df = df.drop(['Longitude', 'Latitude'], axis=1)
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(df, crs=crs, geometry=geometry)


# PART B
#Find intersection between points (accidents) and poligons (zipcodes)
gdfLeft = gpd.read_file(os.path.join(path,zipcodes))
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

# Group by 
Incidents_grouped=Incidents.groupby(['zipcode','Issue Reported']).size()

return Incidents_grouped