from softmax_reg import *
from load import *
from _2048 import _2048
from numpy import * 

cl = softmax_reg_for_2048(16, 4, ops = {'maxiter':3000, 'disp':True})

def softmax_dec(board, u, d, l, r):
    global cl
    p = cl.p_predict(board.flatten(), get_ans = False).flatten()
    if all(board == u[0]):
        p[0] = 0
    if all(board == d[0]):
        p[1] = 0
    if all(board == l[0]):
        p[2] = 0
    if all(board == r[0]):
        p[3] = 0
    p = p / p.sum()
    return random.choice(range(4), p = p)    

if __name__ == '__main__':
    global cl

    tr_x, tr_l = load_data()

    cl.fit(tr_x, tr_l)  

    game = _2048(length = 4)

    game.mul_test(100, softmax_dec, addition_arg = True)
