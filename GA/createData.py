import matplotlib.pyplot as plt
import matplotlib
from numpy import *

DataSize = 30
DataDim = 2
DataRange = 100

if __name__ == '__main__':
    data = random.rand(DataSize, DataDim) * 100
    save('data', data)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(data[:,0], data[:,1], color='red', marker='x', ms=10, ls=' ')
    plt.show()
