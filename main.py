#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 15:20:17 2018

@author: Thomas
"""
#cd ~/desktop/Documents/project#only using iPython console

#import librarys
import numpy as np
from initialise import pyramidYearVect,pyramidMvalues,pyramidFvalues
import plots

#For a year plot the population pyramid 
year=2010
yearPos=sum((pyramidYearVect==year)*np.arange(pyramidYearVect.size))
x1=pyramidMvalues[yearPos,:]
y1=pyramidFvalues[yearPos,:]
plots.plotPyramid(x1,y1)

#Start projection
year=2000 #select starting year
pyramidYearPos=sum((pyramidYearVect==year)*np.arange(pyramidYearVect.size))+1
yearsHist=pyramidYearVect[0:pyramidYearPos:]
#historical data starting year included
pyramidHistM=pyramidMvalues[0:pyramidYearPos,:]
pyramidHistW=pyramidFvalues[0:pyramidYearPos,:]



nProj=10 #number of year of projetion
#Real data on the last year of projection
pyramidProjM=pyramidMvalues[pyramidYearPos+nProj-1,:]
pyramidProjW=pyramidFvalues[pyramidYearPos+nProj-1,:]
#pyramidProjM=projModule.proj2(pyramidHistM,n)

import projModule
#Projection gives the pyramid for each year to the last year of projection
(popProjM,popProjW)=projModule.projPop2(pyramidHistM,pyramidHistW,yearsHist,nProj)
#Plot the pyearmid at the end of the projection with the real data
plots.plot2Pyramid(pyramidProjM,popProjM[nProj,:],pyramidProjW,popProjW[nProj,:])
