import socket
from random import randint

ITER = 500
Data = open('data', 'a')

def record(step, p):
    global Data
    Data.write(repr(p)+','+repr(step)+'\n')

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

    while games < ITER:
        games += 1
        print 'Round%03d:' % games,
        
        panel = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        step = [];

        while True:
            p1.send(repr(panel))
            t = eval(p1.recv(1024))
            panel[t] = 1
            step.append(t);

            if win(panel):
                print 'Player1 wins!', panel
                record(step, 1)
                break
            if draw(panel):
                print 'Draw Games...', panel
                record(step, 0)
                break
    
            p2.send(repr(panel))
            t = eval(p2.recv(1024))
            panel[t] = -1
            step.append(t)
            
            if win(panel):
                print 'Player2 wins!', panel
                record(step, -1)
                break

p1.send('bye')
p2.send('bye')
p1.close()
p2.close()
s.close()
Data.close()
