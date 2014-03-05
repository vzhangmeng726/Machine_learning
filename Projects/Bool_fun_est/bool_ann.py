from numpy import *
from scipy.optimize import minimize
import pso_adv
from operator import le

def f_or(x, y, k = 10.0):
    return log(exp(k * x) + exp(k * y))/k    

def f_and(x, y, k = 10.0):
    return 1 - f_or(1 - x, 1 - y, k) 

def f_or_sim(x, y):
    return x + y - x * y

def f1(i1, i2, para):
#    print i1, i2, para
#    raw_input('hah')
    i1 = int(i1)
    i2 = int(i2)
    tmp = f_or(para[1]*i1+(1-para[1])*(1-i1),para[2]*i2+(1-para[2])*(1-i2))
    return para[0] * tmp + (1 - para[0]) * (1 - tmp) 

def f2(i1, i2, para):
    i1 = int(i1)
    i2 = int(i2)
    return para[0] * f_or(i1, i2) + (1 - para[0]) * f_and(i1, i2)    

def f3(i1, i2, para):
    i1 = int(i1)
    i2 = int(i2)
    return para[0] * f_or_sim(i1, i2) + (1 - para[0]) * (1 - f_or_sim(1-i1, 1-i2))

def L1(a, b):
    return abs(a-b)

def L2(a, b):
    return (a-b) ** 2

class bool_ann(object):
    
    def __init__(self, x, y, ops = {'disp':False, 'maxiter':100},
        f = f1, para_size = 3, min_method = 'L-BFGS-B', train_method = 'scipy'):
        self.total = 0
        self.f = f
        num = x.shape[1]
        while num > 1:
            self.total += num / 2
            num = num/2 + num%2
        
        self.para_size = para_size
        self.para = random.rand(self.total*para_size)
        
        self.x = x
        self.y = y

        if train_method == 'scipy':
            bounds = map(lambda x: (0, 1), self.para)
            self.result = minimize(self.cost, x0 = self.para, bounds = bounds, tol = 0, method = min_method, options=ops)
            self.para = self.result.x.reshape(self.total, self.para_size)
        elif train_method == 'pso':
            self.para = pso_adv.PSO(self.cost, le, lambda: random.rand(self.total * para_size),
                                      20, lambda x: all(x>=0) and all(x<=1), 0.5,
                                      0.8, 2, 2, 1000).get_x()                                                  
                    

    def detail_predict(self, single_x):
        ind = 0
        layer = 0
        l_ori = copy(single_x)
        while ind < self.total:
            print 'layer %d:\t' % layer,
            print l_ori
            print 'para:\t\t',
            layer += 1
            l_tar = [.0] * (len(l_ori)/2 + len(l_ori)%2)
            for ind2 in xrange(len(l_ori)/2):
                l_tar[ind2] = self.f(l_ori[ind2 * 2], l_ori[ind2 * 2 + 1], self.para[ind])
                print self.para[ind],
                ind += 1
            print ''                
            if len(l_ori) % 2 == 1:
                l_tar[-1] = l_ori[-1]
            l_ori = copy(l_tar)

        print 'layer %d:\t' % layer,
        print l_ori


    def cost(self, para):
        error = .0        
        para = para.reshape(self.total, self.para_size)
        for ind, ele in enumerate(self.x):
#            error += L1(self.predict(ele, True), self.y[ind])
            error += L2(self._predict(para, ele, True), float(self.y[ind]))
#        print error,'\r',
        return error                    

    def predict(self, x):
        pre = []
        for ele in x: 
            pre.append( self._predict(self.para, ele) )
        return array(pre)
    
    def _predict(self, para, singal_x, true_value = False):
        ind = 0
        l_ori = copy(map(float, singal_x))
        while ind < self.total:
            l_tar = [.0] * (len(l_ori)/2 + len(l_ori)%2)
            for ind2 in xrange(len(l_ori)/2):
                l_tar[ind2] = self.f(l_ori[ind2 * 2], l_ori[ind2 * 2 + 1], para[ind])
                ind += 1
            if len(l_ori) % 2 == 1:
                l_tar[-1] = l_ori[-1]
            l_ori = copy(l_tar)
        if true_value:
            return l_ori[0]
        else:
            if l_ori[0]>0.5:
                return True
            else:
                return False                    


if __name__ == '__main__':
    x = []
    y = []
    for i in xrange(2**4):
        b = [True, False][random.randint(0, 2)]
        a = b
#        a = [True, False][random.randint(0, 2)]
#        c = [True, False][random.randint(0, 2)]
        d = [True, False][random.randint(0, 2)]        
        c = 1-d

        x.append([a,b])
        y.append(a and b)

#        x.append([a, b, c, d])
#        y.append((a and b) or (c and d))
    x = array(x)
    y = array(y)
    from pprint import pprint
    pprint(zip(x,y))
    cl = bool_ann(x, y, {'disp':False, 'maxiter':100}, f = f3, para_size = 1, train_method = 'scipy')
    cl.detail_predict([True, False])
#    cl.detail_predict([True, False, True, True])
