# -*- coding: utf-8 -*-

from numpy import *
from cPickle import dump

class bool_equ(object):

    def __init__(self, v_size, iter_t):
        self.v_size = v_size
        self.iter_t = iter_t
        self.data = random.randint(0, 2, size = (iter_t, v_size))
        self._not = random.randint(0, 2, size = (iter_t, v_size))

    def __str__(self):
        s = 'v_size: %d, iter_t: %d\nTrue\n' % (self.v_size, self.iter_t)
        tmp_arr = arange(self.v_size)
        for ind, line in enumerate(self.data):
            if line.sum() == 0:
                s += '∧ true\n'
            else:
                s += '∧ ('
                temp_l = []
                for x in tmp_arr[line==1]:
                    if self._not[ind, x]==1:
                        temp_l.append('¬p'+str(x))
                    else:
                        temp_l.append('p'+str(x))
                s += ' ∨ '.join(temp_l) + ')\n'                
        return s                

    def calc(self, x):
        ans = True
        tmp_arr = arange(self.v_size)
        for ind, line in enumerate(self.data):
            if line.sum() != 0:
                line_ans = False
                for ele in tmp_arr[line==1]:
                    if self._not[ind, ele] == 1:
                        line_ans = line_ans or (not x[ele])
                    else:
                        line_ans = line_ans or x[ele]
                ans = ans and line_ans
            if ans == False:
                return False
        return ans                


if __name__ == '__main__':
    
    variables_size = 20
    iteration_times = 70
    equ_size = 1
    data_mul = 2000

    x = []
    y = []
    for i in xrange(equ_size):
        equ = bool_equ(variables_size, iteration_times)
        print ''
        print equ,'='*80
        for t in xrange(data_mul):
#            print t
            ex = random.randint(0, 2, size = (variables_size))
            ey = bool(equ.calc(ex))
            x.append(ex)
            y.append(ey)
#            print ex,ey
    print 'true rate: %lf' % (sum(y)*1.0/len(y))
    dump((array(x),array(y)), open('datas.dat', 'wb', True))            
