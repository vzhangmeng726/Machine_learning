from numpy import *
import ann
import knn

testNum = 40

def loadData():
    global testNum
    a = []

    for lines in open('iris.data'):
        a.append(array(lines.strip().split(',')))
    a = array(a)

    x = a[:,:-1]
    y = a[:,-1]

    distribution = random.permutation(a.shape[0])
    random.shuffle(distribution)
    
    test_x = zeros((testNum, x.shape[1]))
    test_y = array([None] * testNum)
    train_x = zeros((a.shape[0]-testNum, x.shape[1]))
    train_y = array([None] * (y.shape[0]-testNum))

    for ind, ele in enumerate(distribution):
        if (ind < testNum):
            test_x[ind,:] = x[ele,:]
            test_y[ind] = y[ele]
        else:
            train_x[ind-testNum,:] = x[ele,:]
            train_y[ind-testNum] = y[ele]

    return test_x, test_y, train_x, train_y

if __name__ == '__main__':
    global testNum
    test_x, test_y, train_x, train_y = loadData()
    
    print 'test with knn:'
    KNN_Classifier = knn.KNN(train_x, train_y, 1)
    
    correctNum = (KNN_Classifier.predict(test_x) == test_y).sum()
    print 'correct rate = %lf' % (1.0*correctNum/testNum)



    print 'test with ann:'
    ANN_Classifier = ann.NeuralNetworkClassifier([70,70])
    ANN_Classifier.fit(train_x, train_y)

    correctNum = (ANN_Classifier.predict(test_x) == test_y).sum()
    print 'correct rate = %lf' % (1.0 * correctNum / testNum)
