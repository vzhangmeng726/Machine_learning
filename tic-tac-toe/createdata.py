from os import system as s
from time import *
import multiprocessing as mp

def openserver():
    s('python server.py')

def openrandom_player():
    s('python random_player.py')

if __name__ == '__main__':
    a = mp.Process(target=openserver)
    a.start()

    b = mp.Process(target=openrandom_player)
    b.start()

    c = mp.Process(target=openrandom_player)
    c.start()

    a.join()
    b.join()
    c.join()
