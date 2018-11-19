#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 21:06:18 2018

@author: Thomas
"""

import pandas 
#Import pyramid data from csv file
pyramid = pandas.read_csv('importP.csv',sep=';')

#divide the pyramid into Male & Female
male = pyramid['sex']=='M'
female = pyramid['sex']=='F'

pyramidM=pyramid[male]
pyramidF=pyramid[female]

pyramidYearVect=pyramidM['annee'].values #Year vector
                
#For further operation create arrays with values
pyramidMvalues=pyramidM.loc[:,"0":" 105 ou +"].values
pyramidFvalues=pyramidF.loc[:,"0":" 105 ou +"].values
                           