from numpy import *
from matplotlib.pyplot import show, plot

num = load('num.npy')
cv = load('cverror.npy')
test = load('testerror.npy')

plot(num, cv, 'r')
plot(num, test, 'b')
show()
