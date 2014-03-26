from numpy import *

def load_data():
    a = load('rec_board.npy')
    b = load('rec_move.npy')
    print a
    print b

    t = copy(b)
    t[b==0] = 2
    t[b==1] = 3
    t[b==2] = 0
    t[b==3] = 1

    return a.T, t 

if __name__ == '__main__':
    load_data()
