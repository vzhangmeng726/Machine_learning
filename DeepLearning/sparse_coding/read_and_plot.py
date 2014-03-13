import scipy.io as sio
from numpy import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def plot_dig(data, ax, W = None, H = None):
    if W == None:
        W = int(len(data) ** .5)
        H = W
    ax.imshow(data.reshape(H,W), interpolation='none', cmap = cm.gray)       

def rand_plot(data, row = 5, col = 5):
    fig, axs = plt.subplots(row, col, sharex = True, sharey = True)
    for i in xrange(row):
        for j in xrange(col):     
            ind = random.randint(0, data.shape[0])
            plot_dig(data[ind, :], axs[i,j])
    plt.show()
    
def all_plot(data, row = None, col = None):
    l = int(len(data)**0.5)
    fig, axs = plt.subplots(l, l, sharex = True, sharey = True)
    for i in xrange(l):
        for j in xrange(l):
            ind = i*l + j
            plot_dig(data[ind], axs[i,j])
    plt.show()


def load_data(num, dim):
#===========================loading=========================

    data = sio.loadmat('IMAGES.mat')['IMAGES']


#==========================pic=============================

    patch_size = dim
    sample_size = num
    samples = zeros((sample_size, patch_size * patch_size))

    for i in xrange(sample_size):
        ind = random.randint(0, 10)

        x = random.randint(0, 512 - patch_size)
        y = random.randint(0, 512 - patch_size)

        samples[i, :] = data[x:x+patch_size, y:y+patch_size, ind].flatten()

#===========================plot============================

    rand_plot(samples, 2, 2)        
#    all_plot(samples)

    return samples
