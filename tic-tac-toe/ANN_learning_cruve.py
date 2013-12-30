#------------------------
#
#(9) * (40) * (9)
#
#

from numpy import * 
import scipy.optimize as opt

Input_size = 9
Hidden_size = 50
Output_size = 9

X = []
Y = []

def appenddata(y, x):
    def adddata(y, val, label):
        global X, Y
        l = [0]*9
        l[val] = y
        Y.append(copy(l))
        X.append(copy(label))

    label = [0]*9
    flag = 1
    for ind, val in enumerate(x):
        if ind%2 == 0:
            adddata(y, val, label)
        label[val] = flag
        flag = -flag

def randtheta(L_in, L_out):
    epsilon = sqrt(6)/sqrt(L_in+L_out)
    theta = random.rand(L_out, L_in)*2*epsilon - epsilon
    return theta

def sigmoid(x):
    try:
        t = 1.0/(1.0+exp(-x))
    except:
        t = inf
    return t

def logx(x):
    try:
        t = log(x)
    except:
        print t
        t = -inf
    return t

def sigmoidGradient(z):
    return sigmoid(z)*(1.0 - sigmoid(z));

def unroll(theta1, theta2):
    return append(theta1.flatten(),theta2.flatten())

def roll(theta):
    global Input_size, Hidden_size, Output_size

    theta1 = theta[:Input_size*Hidden_size]
    theta1.shape = Hidden_size,-1

    theta2 = theta[Input_size*Hidden_size:]
    theta2.shape = Output_size,-1
    return (theta1, theta2)

def anncostfunction(theta, X, Y):
    m = X.shape[0]

    theta1, theta2 = roll(theta)

    z2 = dot(X, theta1.transpose())
    a2 = sigmoid(z2)
    a3 = sigmoid(dot(a2, theta2.transpose()))

#    print 'X=',X
#    print 'Y=',Y

    delta3 = a3 - Y
#    print 'delta3=',delta3
    delta2 = dot(delta3, theta2) * sigmoidGradient(z2)


#Theta1_grad = 1/m * delta2' * a1 + lambda/m * tmptheta1;
#Theta2_grad = 1/m * delta3' * a2 + lambda/m * tmptheta2;
    theta1_grad = 1.0/m * dot(delta2.transpose(),X)
    theta2_grad = 1.0/m * dot(delta3.transpose(),a2)

    ans =  -1.0/m *sum(Y*logx(a3) + (1-Y)*logx(1-a3))
    ans2 = unroll(theta1_grad, theta2_grad)

#    print ans
    return (ans,ans2)

def predict(X, theta1, theta2):
    H = sigmoid(dot(X, theta1.transpose()))
    Y = sigmoid(dot(H, theta2.transpose()))

    maxx = -1
    for ind, val in enumerate(Y):
        if (X[ind]==0) and (maxx==-1 or Y[maxx]<val):
            maxx = ind
#    print maxx
    return maxx

def calcaccurancy(X, Y, theta1, theta2):
    cor = 0
    m = 0
   # print X.shape[0]
    for ind in xrange(X.shape[0]):
        x = X[ind]
        y = Y[ind]
        m += 1
        if (sum(y)==0):
            cor += 1
        elif (sum(y)==1):
            if (predict(x, theta1, theta2)==list(y).index(y.max())):
                cor += 1
    return cor*1.0/m

def calcerror(X, Y, theta1, theta2):
    acc = 0
    for ind in xrange(X.shape[0]):
        x = X[ind]
        y = Y[ind]

        H = sigmoid(dot(x, theta1.transpose()))
        predicty = sigmoid(dot(H, theta2.transpose()))

        acc += sum( (predicty-y)**2 )
    return 0.5/X.shape[0]*acc

if __name__ == '__main__':
    for line in open('data', 'r'):
        a ,b = eval(line)
        appenddata(a,b)
    X = array(X)
    Y = array(Y)

    theta1 = randtheta(Input_size, Hidden_size)
    theta2 = randtheta(Hidden_size, Output_size)
    
    cvm = 3000*0.2;
    testm = 3000*0.2;
    trainm = 3000*0.6;

    trainX = X[:trainm]
    trainY = Y[:trainm]
    cvX = X[trainm:trainm+cvm]
    cvY = Y[trainm:trainm+cvm]
    testX = X[-testm:]
    testY = Y[-testm:]

#    print map(lambda x: list(x).index(1),Y)

    cverror = []
    testerror = []
    num = []
    i = 0
    ind = 0
    while i < int(trainm):
        theta = opt.minimize(anncostfunction, unroll(theta1, theta2), jac=True,\
                args=(testX[:i+1],testY[:i+1]), \
                method='L-BFGS-B', \
                options={'disp':False})

        theta1, theta2 = roll(theta.x)
        cverror.append(calcerror(cvX, cvY, theta1, theta2) )
        testerror.append(calcerror(testX[:i+1], testY[:i+1], theta1, theta2) )
        num.append(i)
        print i,':',cverror[ind],';',testerror[ind]
        i += 50
        ind += 1

    save('cverror', cverror)
    save('testerror', testerror)
    save('num', num)

    f = open('theta','w')
    f.write(repr(theta1)+','+repr(theta2))
    f.close()
