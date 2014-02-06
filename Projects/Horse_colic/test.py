import ann
import knn
import log_reg
from numpy import *

if __name__ == '__main__':
    data = []
    for line in open('horseColicTraining.txt'):
        data.append(array(map(lambda x: float(x), line.strip().split('\t'))))
    test_data = []
    for line in open('horseColicTest.txt'):
        test_data.append(array(map(lambda x: float(x), line.strip().split('\t'))))
        
    data = array(data)
    test_data = array(test_data)

    x = data[:,:-1]
    y = data[:,-1]    
    test_x = test_data[:,:-1]
    test_y = test_data[:,-1]

#------------    
    anncl = ann.NeuralNetworkClassifier([50,50,20])
    anncl.fit(x, y)
    pre = (anncl.predict(test_x) == test_y).sum()
    print 'ANN: %d/%d' % (pre, test_y.shape[0])

#-----------
    knncl = knn.KNN(x, y, 3)
#    print knncl.predict(test_x)
    pre = (knncl.predict(test_x).flatten() == test_y).sum()
    print 'KNN: %d/%d' % (pre, test_y.shape[0])

#-------------
    logcl = log_reg.Logistic_Regression(x, y, 1.0)
    pre = (logcl.predict(test_x) == test_y).sum()
    print 'Log_reg: %d/%d' % (pre, test_y.shape[0])
