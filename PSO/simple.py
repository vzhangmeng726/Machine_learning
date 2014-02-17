from test_fun import *
from numpy import * 
from operator import le, gt
import pso_adv
import matplotlib.pyplot as plt

def f(x):
    return x**2

def plot(xs, best_pos, best, iteration):
    a = linspace(-5.12, 5.12, 100)
    plt.clf()
    plt.plot(a, map(lambda x: f(x), a), color = 'blue')
    ys = map(lambda x: f(x), xs)
    plt.plot(xs, ys, 'ro')    
    plt.draw()

    plt.pause(0.3)

def plot2(xs, best_pos, best, iteration):
    print iteration, '\t\tf(',best_pos,') =', best,'\r',

#    plt.pause(0.3)

if __name__ == '__main__':   
#    plt.plot(a, map(lambda x: Rastrigin([x]), a))    
#    plt.show()


    plt.ion()
    plt.show()
    x = pso_adv.PSO(f, le, lambda:(random.rand(1)-.5)*10,
            50, lambda x: all(x<5) and all(x>5), 10,
            w = 0.8, c1 = 2, c2 = 2,
            maxiter = 3000,
            plot_f = plot2,
            gen_rate = 0.7, gen_r = 1,
            nor_perceptron = 10, nor_r = 0.3)
