#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 15:20:17 2018

@author: Thomas
"""
#cd ~/desktop/Documents/project#only using iPython console

#import librarys
import pandas
import numpy as np
from initialise import pyramidYearVect,pyramidM,pyramidF,pyramidMvalues,pyramidFvalues
import plots

#For a year plot the population pyramid 
year=2010
yearPos=sum((pyramidYearVect==year)*np.arange(pyramidYearVect.size))
x1=pyramidMvalues[yearPos,:]
y1=pyramidFvalues[yearPos,:]
plots.plotPyramid(x1,y1)

    




#Project population First approach using death and born data found on official statistical agencies
"""
from deathData import deathYearVect,deathM,deathF
import projModule
year=1990 #select starting year
pyramidYearPos=sum((pyramidYearVect==year)*np.arange(pyramidYearVect.size))
deathYearPos=sum((deathYearVect==year)*np.arange(deathYearVect.size))

#data at the initial year
year0M=pyramidMvalues[pyramidYearPos,:]
year0W=pyramidFvalues[pyramidYearPos,:]

nProj=10 #Number of year projected
yearM_proj=np.zeros((year0M.size,nProj+1))
yearW_proj=np.zeros((year0W.size,nProj+1))

yearM_proj[:,0]=year0M
yearW_proj[:,0]=year0W

for iYear in range(1,nProj+1):

    #proj data at year +nProj
    deathRatesM=deathM[deathYearPos+iYear]
    deathRatesW=deathM[deathYearPos+iYear]
    
    yearM_proj[:,iYear]=projModule.projPop1(yearM_proj[:,iYear-1],deathRatesM)
    yearW_proj[:,iYear]=projModule.projPop1(yearW_proj[:,iYear-1],deathRatesM)
    

year1M_real=pyramidMvalues[pyramidYearPos+nProj,:]
year1W_real=pyramidFvalues[pyramidYearPos+nProj,:]
#Plot male at n+1 to compare
plots.plot2Pyramid(year1M_real,yearM_proj[:,nProj],year1W_real,yearW_proj[:,nProj])
"""

#Second approach is to project population considering only the past pyramid and evaluate the variables
#import projModule decoment latter
year=2000 #select starting year
pyramidYearPos=sum((pyramidYearVect==year)*np.arange(pyramidYearVect.size))+1
yearsHist=pyramidYearVect[0:pyramidYearPos:]
#historical data until and starting year included
pyramidHistM=pyramidMvalues[0:pyramidYearPos,:]
pyramidHistW=pyramidFvalues[0:pyramidYearPos,:]



#Output is the pyramid for year start+1 to n
nProj=10 #number of year of projetion
pyramidProjM=pyramidMvalues[pyramidYearPos+nProj-1,:]
pyramidProjW=pyramidFvalues[pyramidYearPos+nProj-1,:]
#pyramidProjM=projModule.proj2(pyramidHistM,n)
'''beg'''
n=nProj
PopM=pyramidHistM
PopW=pyramidHistW
import numpy as np
import pandas
import statistics

BYpower = pandas.read_csv('~/Desktop/Documents/Project/BYpower.csv',sep=';')

yearHist=PopM[:,1].size
BirthRate=np.zeros((yearHist-1))#Container for the annual birth rate 
MFratioTab=np.zeros((yearHist-1))#Container for the ratio between male and female
for iYear in range(1,yearHist):
    #Birth rate as a % of population between 18 to 45
    BirthN=PopW[iYear,0]+PopM[iYear,0]
    AvgMF=(sum(PopW[iYear-1,17:44])+sum(PopM[iYear-1,17:44]))/2
    BirthRate[iYear-1]=BirthN/AvgMF
    MFratioTab[iYear-1]=PopM[iYear,0]/(PopW[iYear,0]+PopM[iYear,0])
        
MFratioHist=statistics.mean(MFratioTab)
    #plots.plotFunL(yearsHist[0:-1],BirthRate)
    
d=np.zeros((yearHist-1,2))
d[:,0]=yearsHist[0:-1]
d[:,1]=BirthRate

birthToMerge=pandas.DataFrame(d,columns=['Year', 'birthRate'])
    
    
Merged=BYpower.set_index('Year').join(birthToMerge.set_index('Year'))
Merged=Merged[Merged["birthRate"]>-10]#To remove columns with missing data
Merged=Merged[Merged["Bypower"]>-10]#To remove columns with missing data
BirthBYpower=Merged.values

    #Normalize the data
BYmean=statistics.mean(BirthBYpower[:,0])
BYstdev=statistics.stdev(BirthBYpower[:,0])
birthRateMean=statistics.mean(BirthBYpower[:,1])
birthRateStdDev=statistics.stdev(BirthBYpower[:,1])
    
    
BirthBYpower[:,1]=(BirthBYpower[:,1]-birthRateMean)/birthRateStdDev
BirthBYpower[:,0]=(BirthBYpower[:,0]-BYmean)/BYstdev
    
    #plots.scatterPlot(BirthBYpower)
    #perform regression
z = np.polyfit( BirthBYpower[:,0],BirthBYpower[:,1], 1)
p=np.poly1d(z)
    #vectorProj=np.arange(-2,2,0.1)
    #regressionPoints=np.zeros((40))
    #regressionPoints=p(vectorProj)
    #import matplotlib.pyplot as plt
    #plt.scatter(BirthBYpower[:,0], BirthBYpower[:,1])
    #plt.plot(regressionPoints,vectorProj)
    #plt.show
    #Output = buying power
"""export birth rate by taking the BYpower of future years (could be an estimation)"""
futureYears=yearsHist[-1:]
yearStart=yearsHist[yearsHist.size-1]
futureBYpower=np.zeros((n))
for iYear in range(0,n):
    futureYears=np.append(futureYears,yearStart+iYear)
    futureBYpower[iYear]=BYpower[BYpower["Year"]==(yearStart+iYear)].Bypower
    #Transform apply the polynom and convert again in birth rate
futureBYpower=(futureBYpower-BYmean)/BYstdev
futureBirthRate=p(futureBYpower)
futureBirthRate=futureBirthRate*birthRateStdDev+birthRateMean
#for i in range(0,futureBirthRate.size):
#    futureBirthRate[i]=BirthRate[yearHist-2]
    


'''end'''
import projModule
(popProjM,popProjW)=projModule.projPop2(pyramidHistM,pyramidHistW,yearsHist,nProj)
plots.plot2Pyramid(pyramidProjM,popProjM[nProj,:],pyramidProjW,popProjW[nProj,:])
#plots.plotPyramid(popProjM[nProj,:],popProjW[nProj,:])
