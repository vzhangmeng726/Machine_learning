import socket
from random import shuffle
from numpy import *

def avail(p):
    ans = []
    for ind, val in enumerate(p):
        if val==0:
            ans.append(ind)
    return ans

def sigmoid(x):
    return 1.0/(1.0+exp(-x))

if __name__ == '__main__':
    f = open('theta_100_iter50','r')
    theta1, theta2 = eval(f.read())
    f.close()

    s = socket.socket()

    f = open('port', 'r')
    s.connect((socket.gethostname(), eval(f.read())))
    f.close()

    print 'Successfully connect!'
    while True:
        rec = s.recv(1024)
        try:
            X = eval(rec)

            H = sigmoid(dot(X, theta1.transpose()))
            Y = sigmoid(dot(H, theta2.transpose()))

            maxx = -1
            for ind, val in enumerate(Y):
                if (X[ind]==0) and (maxx==-1 or Y[maxx]<val):
                    maxx = ind
            #print maxx
            
            s.send(repr(maxx))
        except:
            if rec=='bye':
                break

    s.close()


