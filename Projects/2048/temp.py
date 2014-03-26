from numpy import *

if __name__ == '__main__':
    a = load('rec_board.npy')
    b = load('rec_move.npy')
    print a.shape
    print b.shape

    t = copy(b)
    t[b==0] = 2
    t[b==1] = 3
    t[b==2] = 0
    t[b==3] = 1
    print t[:10]
    print b[:10]
