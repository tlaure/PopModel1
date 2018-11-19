def plotPyramid(x1,y1) :
    import matplotlib.pyplot as plt
    import numpy as np
    y = np.arange(x1.size)
    fig, axes = plt.subplots(ncols=2, sharey=True)
    axes[0].barh(y, x1/1000, align='center', color='xkcd:steel blue')
    axes[0].set(title='Number of Male')
    axes[1].barh(y, y1/1000, align='center', color='xkcd:purplish')
    axes[1].set(title='Number of Female')
    axes[0].invert_xaxis()
    axes[0].yaxis.tick_right()
    plt.show()
    
def plot2Pyramid(x1,x2,y1,y2) :
    import matplotlib.pyplot as plt
    import numpy as np
    y = np.arange(x1.size)
    fig, axes = plt.subplots(ncols=2, sharey=True)
    axes[0].barh(y, x1/1000, align='center', alpha=0.5, color='xkcd:steel blue')
    axes[0].barh(y, x2/1000, alpha=0.5, color='xkcd:light grey')
    axes[0].set(title='Number of Male')
    axes[1].barh(y, y1/1000, align='center', alpha=0.5, color='xkcd:purplish')
    axes[1].barh(y, y2/1000, align='center', alpha=0.5, color='xkcd:clay')
    
    axes[1].set(title='Number of Female')
    
    axes[0].invert_xaxis()
    axes[0].yaxis.tick_right()
    
    plt.show()
    
def plotFun(y):
    import matplotlib.pyplot as plt
    plt.plot(y)
    plt.show()
    
def plotFunL(y,x):
    import matplotlib.pyplot as plt
    plt.plot(y,x)
    plt.show()
        
def plotNhor(array,step):
    import matplotlib.pyplot as plt
    for i in range(0,array[:,0].size,step):
        plt.plot(array[i,:],label=str(i))
    plt.show()
    
def plotNvert(array,step):
    import matplotlib.pyplot as plt
    import numpy as np
    for i in range(0,array[0,:].size,step):
        plt.plot(array[:,i],label=str(i))
        
    plt.legend([np.arange(array[0,:].size,step)])
    plt.show()
    
def scatterPlot(Array):
    import matplotlib.pyplot as plt
    plt.scatter(Array[:,0], Array[:,1])
    plt.show