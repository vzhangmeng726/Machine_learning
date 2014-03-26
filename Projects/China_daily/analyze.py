from numpy import *
from pprint import pprint
from numpy import *
import nb
import re
import pickle
import apriori

if __name__ == '__main__':
    stoplist = []
    for ele in open('stoplist.dat', 'r'):
        stoplist.append(ele[:-1])
    stoplist.extend(['htm', 'cn', '_blank', 'href', 'target', 'http'])

    d = pickle.load(open('shrinked_200_3.dat', 'rb'))
        
    x = []
    y = []
    my_list = ['China News', 'China News', 'China News', \
               'China News', 'China News', 'World News', \
               'China News', 'China News', 'World News', \
               'World News', 'China News', 'World News']

    ori_list = ['Bizchina News', 'Photo News', 'Sports News', \
                'Life News', 'China Daily News', 'World News', \
                'Entertainment News', 'Opinion News', 'China Daily USA News', \
                'HK Edition News', 'China News', 'China Daily European Weekly News']
    for kind in d:
        for ele in d[kind]:
            x.append([word.lower() for word in re.split(r'\W*', ele[1]) if len(word)>1 and not word.lower() in stoplist])
#            y.append(my_list[ori_list.index(kind)])   
            y.append(kind)
    ''' 'Bizchina News', 'Photo News', 'Sports News', 'Life News', 'China Daily News', 'World News', 'Entertainment News', 'Opinion News', 'China Daily USA News', 'HK Edition News', 'China News', 'China Daily European Weekly News' '''
    x = array(x)
    y = array(y)
    m = x.shape[0]
    randind = random.permutation(m)
    x = x[randind]
    y = y[randind]

    print 'apriori is finding connection...'
#    ap = apriori.Apriori(map(set, x[y=='World News']), 0.04, 0.6)
    ap = apriori.Apriori(map(set, x), 0.04, 0.8)
    pprint(ap.freq_set()[0])
    ap.pprint_rules()


    training_rate = 0.8
    split_ind = m * training_rate
    train_x = x[:split_ind]
    train_y = y[:split_ind]
    test_x = x[split_ind:]
    test_y = y[split_ind:]    

    print 'training...'
    nb_cl = nb.NaiveBayes(list(train_x), list(train_y))
    print 'predicting...'
    correct = 0
    for ele, ans in zip(test_x, test_y):
        pre, pro = nb_cl.classify(ele)
        #print ele, pre, ans
        correct += (ans == pre)        
    print 'correct: %d/%d = %lf' % (correct, len(test_y), correct*1.0/len(test_y))
