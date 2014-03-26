from cPickle import load
from numpy import *
import ann
import adaboost
import bool_ann

if __name__ == '__main__':
    print '...loading datas'
    x, y = load(open('datas.dat', 'rb'))
    rate = 0.8
    spInd = x.shape[0] * rate
    test_s = x.shape[0] - spInd + 1

    print 'traing data: %d, testing data: %d' % (spInd-1, test_s)
    print 'the true rate: %lf' % ((y==True).sum()*1.0/y.shape[0])


#    print '======Test with Bool_ANN======='
#    classifier = bool_ann.bool_ann(x[:spInd], y[:spInd],{'disp':False, 'maxiter':10})
#    correct = (classifier.predict(x[spInd:])==y[spInd:]).sum()
#    print 'correct = %d/%d = %lf' % (correct, test_s, correct*1.0/test_s)

    print '======Test with ANN========'
    classifier = ann.NeuralNetworkClassifier([50])
    classifier.fit(x[:spInd], y[:spInd])
    correct = (classifier.predict(x[spInd:]) == y[spInd:]).sum()
    print 'correct = %d/%d = %lf' % (correct, test_s, correct*1.0/test_s)


    print '======Test with Adaboost======='
    new_y = array(map(lambda y: (y-0.5)*2, y))
    classifier = adaboost.AdaBoost(x[:spInd], new_y[:spInd], adaNum = 200)
    pre = classifier.predict(x[spInd:])
    correct = (pre == y[spInd:]).sum()
    print 'correct = %d/%d = %lf' % (correct, test_s, correct*1.0/test_s)
    



