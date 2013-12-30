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
    return 1.0/(1.0+exp(-x))

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

def anncostfunction(theta):
    global X, Y
    m = X.shape[0]
 
    theta1, theta2 = roll(theta)
    z2 = dot(X, theta1.transpose())
    a2 = sigmoid(z2)
    a3 = sigmoid(dot(a2, theta2.transpose()))
    
    ans =  -1.0/m *  sum(Y*log(a3) + (1-Y)*log(1-a3))
#    print ans,
#J = -1/m * sum(sum(Y .* log(a3) + (onek .- Y).*log(onek.-a3)))...
#        + lambda/(2*m) * (sum(sum((Theta1.^2)(:,2:end)))+sum(sum((Theta2.^2)(:,2:end))) );
#    print 'X=',X
#    print 'Y=',Y

    delta3 = a3 - Y
#    print 'delta3=',delta3
    delta2 = dot(delta3, theta2) * sigmoidGradient(z2)


#Theta1_grad = 1/m * delta2' * a1 + lambda/m * tmptheta1;
#Theta2_grad = 1/m * delta3' * a2 + lambda/m * tmptheta2;
    theta1_grad = 1.0/m * dot(delta2.transpose(),X)
    theta2_grad = 1.0/m * dot(delta3.transpose(),a2)

    ans2 = unroll(theta1_grad, theta2_grad)

#    print ans
    return (ans, ans2)
    

if __name__ == '__main__':
    for line in open('data', 'r'):
        a ,b = eval(line)
        appenddata(a,b)
    X = array(X)
    Y = array(Y) 

    theta1 = randtheta(Input_size, Hidden_size)
    theta2 = randtheta(Hidden_size, Output_size)
    
#    theta = opt.fmin_bfgs(anncostfunction, unroll(theta1, theta2), maxiter=100, fprime=anngrad)
    theta = opt.minimize(anncostfunction, unroll(theta1, theta2),jac=True, method='L-BFGS-B',options={'disp':True,'maxiter':150})

    theta1, theta2 = roll(theta.x)

    f = open('theta','w')
    f.write(repr(theta1)+','+repr(theta2))
    f.close()
