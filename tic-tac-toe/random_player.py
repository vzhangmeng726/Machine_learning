import socket
from random import shuffle

def avail(p):
    ans = []
    for ind, val in enumerate(p):
        if val==0:
            ans.append(ind)
    return ans

if __name__ == '__main__':
    s = socket.socket()

    f = open('port', 'r')
    s.connect((socket.gethostname(), eval(f.read())))
    f.close()

    print 'Successfully connect!'
    while True:
        rec = s.recv(1024)
        try:
            p = avail(eval(rec))
            shuffle(p)
            t = p[0]
            s.send(repr(t))
        except:
            if rec=='bye':
                break

    s.close()
