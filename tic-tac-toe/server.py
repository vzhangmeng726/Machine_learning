import socket
from random import randint
from time import sleep

ITER = 3000
Data = open('data', 'w')
Sat = [.0, .0, .0]
P1mark = 1 
P2mark = -1
P1winmark = 1
P2winmark = -1
Drawmark = 0

def record(step, p):
    global Data
    Data.write(repr(p)+','+repr(step)+'\n')
    pass

def win(a):
    return (a[0]==a[1]==a[2]!=0 or a[3]==a[4]==a[5]!=0 or a[6]==a[7]==a[8]!=0 or\
            a[0]==a[3]==a[6]!=0 or a[1]==a[4]==a[7]!=0 or a[2]==a[5]==a[8]!=0 or\
            a[0]==a[4]==a[8]!=0 or a[2]==a[4]==a[6]!=0)

def draw(a):
    return a.count(0)==0

if __name__ == '__main__':
    host = socket.gethostname()
    port = randint(2000, 5000)
    f = open('port', 'w')
    f.write(repr(port))
    f.close()

    s = socket.socket()
    s.bind((host,port))
    print 'Waiting for Players...'
    s.listen(3)
    p1 = s.accept()[0]
    print 'Player1 is ready'
    p2 = s.accept()[0]
    print 'Player2 is ready'

    games = 0
    global ITER
    global Sat, P1mark, P2mark, P1winmark, P2winmark, Drawmark

    while games < ITER:
        games += 1
#        print 'Round%03d:' % games, '\r',
        
        panel = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        step = [];

        while True:
            p1.send(repr(panel))
            t = eval(p1.recv(1024))
            panel[t] = P1mark
            step.append(t);

            if win(panel):
                record(step, P1winmark)
                Sat[1] += 1
                break
            if draw(panel):
                record(step, Drawmark)
                Sat[0] += 1
                break
    
            p2.send(repr(panel))
            t = eval(p2.recv(1024))
            panel[t] = P2mark
            step.append(t)
            
            if win(panel):
                record(step, P2winmark)
                Sat[2] += 1
                break
        print 'P1win=%.6lf;P2win=%.6lf;Draw=%.6lf\r' % (Sat[1]/games,Sat[2]/games,Sat[0]/games),
print '\n'
p1.send('bye')
p2.send('bye')
p1.close()
p2.close()
s.close()
Data.close()
