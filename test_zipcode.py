#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 14:14:34 2019

@author: mikaelapisanileal
"""

from uszipcode import SearchEngine

lat = 33.577862
lon = -101.855164
search = SearchEngine(simple_zipcode=False)
result = search.by_coordinates(lat, lon, radius=30)

zipcodes = []
for x in result:
    zipcodes.append((x.zipcode,x.radius_in_miles))

zipcodes.sort(key=lambda x: x[1])
    
zipcodes[0][0]    









