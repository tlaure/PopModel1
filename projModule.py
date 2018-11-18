#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 19:02:47 2018

@author: Thomas
"""

def projPop1(pop0,deathRates): #1ere approche simpliste
    #pop0 is population as of 1of january t
    
    import numpy as np
    
    pop0AfterDeath=pop0-pop0**deathRates
    newBorn = np.array([0])
    popBeforeNewBorn=pop0AfterDeath[:pop0AfterDeath.size-1]
    pop0AfterYear=np.concatenate((newBorn,popBeforeNewBorn), axis=0)
    return(pop0AfterYear)


def projPop2(popHistM,popHistW,yearsHist,n): 
    #To project the population this function use the historical pyramid
    #Evaluate the death rate function at each age using regressions
    #Evaluate the number of newborn based on a regression of each years birth according to n# of woment between 16to50
    import pandas
    import numpy as np
    #Call the function for the mortality rates
    mortalityRatesM=projMortalityRates(popHistM,n)
    mortalityRatesW=projMortalityRates(popHistW,n)
    BYpower = pandas.read_csv('~/Desktop/Documents/Project/BYpower.csv',sep=';')
    (futureBirthRate,BirthMFratio)=projBirth(popHistM,popHistW,yearsHist,n,BYpower)
    nAges=popHistM[0,:].size
    yearHist=popHistM[:,0].size
                  
    popProjM=np.zeros((n+1,nAges))
    popProjW=np.zeros((n+1,nAges))
    #First element is the last year of historic data
    popProjM[0,:]=popHistM[yearHist-1,:]
    popProjW[0,:]=popHistW[yearHist-1,:]
    
    """Begin loop on each year to project pop"""
    for iYear in range(1,n+1):
        #Begin with the birth that happen during the first year
        AvgMF=(sum(popProjM[iYear-1,17:44])+sum(popProjW[iYear-1,17:44]))/2
        print(AvgMF)
        birthYear=AvgMF*futureBirthRate[iYear-1]
        print(futureBirthRate[iYear-1])
        popProjM[iYear,:]=projDeathAndAging('M',popProjM[iYear-1,:],mortalityRatesM[iYear-1],birthYear,BirthMFratio)
        popProjW[iYear,:]=projDeathAndAging('F',popProjW[iYear-1,:],mortalityRatesW[iYear-1],birthYear,BirthMFratio)
    return(popProjM,popProjW)


def projDeathAndAging(S,pop0,deathRates,birthYear,BirthMFratio): #1ere approche simpliste
    #pop0 is population as of 1of january t
    
    import numpy as np
    
    
    if S=='M':
        newBorn = np.array([birthYear*BirthMFratio])
    else:
        newBorn = np.array([birthYear*(1-BirthMFratio)])
    
    popBeforeNewBorn=np.zeros((pop0.size))
    for i in range(0,pop0.size-2):
        popBeforeNewBorn[i+1]=pop0[i]-pop0[i]*deathRates[i]
        
    popBeforeNewBorn[0]=newBorn
    return(popBeforeNewBorn)
    
    
def projMortalityRates(popHist,n):
    import numpy as np
    #import plots
    yearHist=popHist[:,1].size
    nAgePyramid=popHist[1,:].size
    ages=np.arange(0,nAgePyramid)
    mortalityRatesHist=np.zeros((yearHist-1,nAgePyramid))#Container for the mortality rates, ordered from most recent to older rates
    mortalityRatesHistClean=np.zeros((yearHist-1,nAgePyramid))#Container for the mortality rates, ordered from most recent to older rates
    
    for iYear in range(1,yearHist):
        for iAge in range(1,nAgePyramid):
            #1-popAgeN@t/popAgeN-1@t is the mortality rate for N-1@t-1 as is the % of pop which haven't survived
            if popHist[iYear-1,iAge-1]==0:
                mortalityRatesHist[iYear-1,iAge-1]=0
            else:
                mortalityRatesHist[iYear-1,iAge-1]=1-popHist[iYear,iAge]/popHist[iYear-1,iAge-1]
        #Fit a polynomal regtession from year 0 to last survival year -2 as the last two value may lead to some issues
        #start by cleaning the end of the vector including the two last data
        yearEnd=nAgePyramid-1
        
        while (mortalityRatesHist[iYear-1,yearEnd]==0):
            yearEnd=yearEnd-1
        #Perform regression
        x=ages[0:yearEnd-2]
        y=mortalityRatesHist[iYear-1,0:yearEnd-2]
        z = np.polyfit(x, y, 5)
        p=np.poly1d(z)#Polynom for the mortality rates at year iYear
        mortalityRatesHistClean[iYear-1,:]=p(ages)
    #Plot mortality rate across ages for fixed period and evolution of mortality rate by age during the past
    #plots.plotNvert(mortalityRatesHistClean,10)
    #plots.plotNhor(mortalityRatesHistClean,10)
    #Project mortality rates for upcomming periods 
    #following the graph use a linear regression across the periods
    mortalityRatesProj=np.zeros((n,nAgePyramid))
    vectorHist=np.arange(0,yearHist-1)
    vectorProj=np.arange(yearHist+1,yearHist+1+n)
    for iAge in range(0,nAgePyramid):
        y=mortalityRatesHistClean[:,iAge]
        x=vectorHist
        z = np.polyfit(x, y, 1)
        p=np.poly1d(z)
        mortalityRatesProj[:,iAge]=p(vectorProj)
        
    #plots.plotNhor(mortalityRatesProj,1)
    #plots.plotNhor(mortalityRatesHistClean,1)
    return(mortalityRatesProj)
    
def projBirth(PopM,PopW,yearsHist,n,BYpower):
    import numpy as np
    import pandas
    import statistics
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
    z = np.polyfit(BirthBYpower[:,0], BirthBYpower[:,1], 1)
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
    return(futureBirthRate,MFratioHist)
    