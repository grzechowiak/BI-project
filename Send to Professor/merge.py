#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 16:21:48 2019

@author: mikaelapisanileal
"""

def merge_data(df1,df2,d3,df4,df5):
    
    ## MERGING
    
    #MERGE df1 + df2
    #Merge right join. We want everything from df2 and join to it df1
    df1_2=pd.merge(df1, df2, how='right', left_on=['Zip Code'], right_on=['Postal Code'])
    df1_2.count()
    #We don't need column "Zip Code" from column, we're gonna use Postal Code from df2 
    df1_2=df1_2.drop(columns=["Zip Code"])
    len(df1_2.columns) # Check