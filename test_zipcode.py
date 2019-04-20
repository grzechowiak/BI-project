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
result = search.by_coordinates(lat, lon, radius=30, returns=5)

for x in result:
    print(x.zipcode)
    









