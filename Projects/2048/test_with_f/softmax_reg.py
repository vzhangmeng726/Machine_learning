from numpy import *
from scipy.optimize import minimize

class softmax_reg_for_2048(object):
                    
    def __init__(self, inputSize, numClasses, lmbd = 1e-4, ops = {'maxiter':200, 'disp':True}):
        self.lmbd = lmbd
        self.ops = ops
        self.inputSize = self.convolution(zeros((inputSize, 1))).shape[0]
        self.numClasses = numClasses
        self.theta = 0.005 * random.normal(0, 1, (self.numClasses * self.inputSize, 1))
        pass

    @staticmethod
    def convolution(x):
        return x
        def dist(x, y):
            return 0

        ans = []
        for ind in xrange(x.shape[1]):
            ele = x[:, ind].reshape(int(x.shape[0] ** .5), -1)
            addition = []
            for i in xrange(4):
                for j in xrange(4):
                    if i+1 < 4:
                        addition.append( dist(ele[i, j], ele[i+1, j]))
                    if j+1 < 4:
                        addition.append( dist(ele[i, j], ele[i, j+1]))
            ans.append ( list(ele.flatten())+(addition) ) 
        #    ans.append(addition)
        return array(ans).T            

    def fit(self, data, labels):
        self.data = self.convolution(data)
        self.labels = labels

        self.result = minimize(self.cost, x0 = self.theta,
                        method = 'L-BFGS-B', jac = True,
                        options = self.ops, tol = 1e-100)
        self.theta = self.result.x.reshape(self.numClasses, self.inputSize)

    def sgd_fit(self, data, labels, alpha = 0.1):
        self.theta = self.theta.reshape(-1, 1)

        self.data = data
        self.labels = labels
        cost, grad = self.cost(self.theta)
        self.theta -= alpha * grad.reshape(-1, 1)

        self.theta = self.theta.reshape(self.numClasses, self.inputSize)

    def cost(self, theta):
        theta = theta.reshape(self.numClasses, self.inputSize)

        numCases = self.data.shape[1]
        groundTruth = zeros((self.numClasses, numCases))       
        for ind, ele in enumerate(self.labels):
            groundTruth[ele, ind] = 1            

        n, m = self.data.shape
        M = dot(theta, self.data)
        M -= M.max(0)

        M = exp(M)

        p = M / M.sum(0)


        cost = -1.0 / m * dot(groundTruth.flatten().T, log(p.flatten())) + self.lmbd / 2 * sum(theta ** 2)
        thetagrad = - 1.0 / m * dot( (groundTruth - p), self.data.T) + self.lmbd * theta    

#        print theta.flatten()
#        print thetagrad.flatten()

        return cost, thetagrad.flatten()        

    def predict(self, data):
        data = self.convolution(data)
        M = dot(self.theta, data)
#        print M.argmax(0)
        return M.argmax(0)

    @staticmethod
    def sigmoid(z):
        return 1.0/(1+exp(-z))

    def p_predict(self, data, get_ans = True):               
        data = self.convolution(data.reshape(-1,1))

        M = dot(self.theta, data)
#        M = self.sigmoid(M * 10)
        M = exp(M)
        p = (M / M.sum(0)).reshape(-1, 1)
        if not get_ans:
            return p
        ans = []
        for ind in xrange(p.shape[1]):
            ans.append(random.choice(arange(self.numClasses), p = p[:,ind]))
        if get_ans:            
            return array(ans)

if __name__ == '__main__':

    tr_x, tr_l, test_x, test_l = rap.load_data(num = 100, threshold = 1)
    cl = softmax_reg(28 * 28, 10)

    cl.fit(tr_x, tr_l)
    pre = cl.p_predict(test_x)
    cor = sum(pre == test_l)
    print 'correct: %d / %d = %lf' % ( cor, test_l.shape[0], float(cor)/test_l.shape[0])

    '''
    #sgd training
    for i in xrange(100):   
        ind = random.randint(0, 1000, 10)
        cl.sgd_fit(tr_x[:, ind], tr_l[ind], alpha = 0.05)

        pre = cl.predict(test_x)
        cor = sum(pre == test_l)
        print 'correct: %d / %d = %lf' % ( cor, test_l.shape[0], float(cor)/test_l.shape[0])
    '''        
    
    '''
#grad test
    cl = softmax_reg(4, 2, 1e-4)
    cl.data = array([[1, 0, 2],[0, 1, 2],[0, 1, 3],[1, 0, 3]])
    cl.labels = array([0, 1, 0])
    t =  cl.cost(array([0,1,1,0,0,1,1,0]))

    done:octave flatten('F') while python flatten('C')
    '''
