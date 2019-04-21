#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 17:09:34 2019

@author: mikaelapisanileal
"""

from uszipcode import SearchEngine
import numpy as np

def get_zipcode(row):   
    search = SearchEngine(simple_zipcode=False)
    result = search.by_coordinates(row['Latitude'],row['Longitude'])
    zipcodes = []
    for x in result:
        zipcodes.append((x.zipcode,x.radius_in_miles))
    
    zipcodes.sort(key=lambda x: x[1])
    if len(zipcodes) == 0:
        return -1
    else:
        return zipcodes[0][0]


#clean traffic data and create new column zipcode
def get(df):
    # keep columns 'Issue Reported', 'Latitude', 'Longitude'
    df = df[['Issue Reported', 'Latitude', 'Longitude', 'Status Date']]
    
    # keep month = March and Year = 2019
    df['Date'] = df['Status Date'].str.extract('\d{2}/\d{2}/(\d{4}) *')
    df = df[(df.Date == '2019')]
    df['Month'] = df['Status Date'].str.extract('(\d{2})/\d{2}/\d{4} *')
    df = df[(df.Month == '03')]
    
    # remove lat=0 long=0
    df = df[(df.Latitude != np.float64(0)) & (df.Longitude != np.float64(0))]
    
    #add column zipcode
    df['ZipCode'] = df.apply(get_zipcode, axis = 1)
    df = df[['ZipCode', 'Issue Reported', 'Latitude', 'Longitude']]

    return df

