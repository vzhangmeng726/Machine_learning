from os import system as s
import multiprocessing as mp

if __name__ == '__main__':
    a = mp.Process(target=s('python server.py'))
    b = mp.Process(target=s('python random_player.py'))
    c = mp.Process(target=s('python random_player.py'))
    a.start()
    b.start()
    c.start()
    a.join()
    b.join()
    c.join()
