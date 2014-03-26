import pygame
from pygame.locals import *
from sys import exit
from numpy import *
import sys 

rec_board = list(load('rec_board.npy'))
rec_move = list(load('rec_move.npy'))

class _2048(object):    

    def check(self, f):
        tmp = f()
        if all(tmp == self.board):
            return False
        else:
            self.board = tmp.copy()
            return True
    

    def change(self):
        self.screen.fill((255, 238, 240))
#        self.screen.fill((182, 255, 0))
        
        if (self.board == 0).sum() > 0:
            rx = random.randint(0, self.a)
            ry = random.randint(0, self.a)
            while (self.board[rx, ry] != 0):
                rx = random.randint(0, self.a)
                ry = random.randint(0, self.a)
            self.board[rx, ry] = 2 ** random.choice([1,2], 1, p=[0.9, 0.1])
        
        for i in xrange(self.a):
            for j in xrange(self.a):
#                if self.board[i, j] != 0:
                self.screen.blit(self.block[self.board[i, j]], (j * (self.block_a + self.margin) + self.margin,\
                                                                      i * (self.block_a + self.margin) + self.margin))
#    print board                                
        pygame.display.update()


    def create_digitals(self):
        k = array([0, 148, 255])
        w = array([255, 255, 255])
        f = pygame.font.SysFont('ubuntu', int(0.4 * self.block_a))
        dig = {}
        for i in arange(20):
            num = 2 ** i

            bg = pygame.surface.Surface((self.block_a, self.block_a))
            bg.fill(tuple(k + (w - k) * float(19-i)/20))
            ts = f.render(str(num), True, (0, 0, 0))
            bg.blit(ts, ((bg.get_width()-ts.get_width())/2, (bg.get_height()-ts.get_height())/2))
            
            pygame.image.save(bg, str(num)+'.png')
            dig[num] = bg
#        dig[num] = pygame.image.load(str(num)+'.png').convert_alpha()

        zero = pygame.surface.Surface((self.block_a, self.block_a))
        zero.fill((218, 255, 127))
        dig[0] = zero
        return dig       

    @staticmethod
    def gravity(l):
        p = 0
        new_l = []
        ind = 0
        stack = 0
        for ele in l:
            if ele == 0:
                pass
            elif ele == stack:
                new_l.append(stack * 2)
                p += stack * 2
                stack = 0
            elif stack != 0:
                new_l.append(stack)
                stack = ele
            else:
                stack = ele                    
        if stack != 0 :
            new_l.append(stack)
        return new_l, p

    def left(self):
        tmp = self.board.copy()
        for i in xrange(self.a):
            l = array(self.gravity(tmp[i, :])[0])
            tmp[i, :] = zeros(self.a)
            tmp[i, :len(l)] = l
        return tmp           

    def up(self):
        tmp = self.board.copy()
        for i in xrange(self.a):
            l = array(self.gravity(tmp[:, i])[0])
            tmp[:, i] = zeros(self.a).T
            tmp[:len(l), i] = l.T
        return tmp                      
            
    def right(self):
        tmp = self.board.copy()
        for i in xrange(self.a):
            l = array(self.gravity(tmp[i, ::-1])[0])
            tmp[i, :] = zeros(self.a)
            tmp[i, ::-1][:len(l)] = l
        return tmp                      

    def down(self):
        tmp = self.board.copy()
        for i in xrange(self.a):
            l = array(self.gravity(tmp[::-1, i].T)[0])
            tmp[:, i] = zeros(self.a).T
            tmp[::-1, i][:len(l)] = l.T
        return tmp                     
    '''        def left(self, return_point = False):
            point = 0
            tmp = self.board.copy()
            for i in xrange(self.a):
                ind0 = 0
                indx = 0
                while indx + 1 < self.a:
                    if tmp[i, indx] == tmp[i, indx + 1]:                        
                        tmp[i, indx] = 0
                        tmp[i, indx + 1] = 0
                        
                        tmp[i, ind0] = tmp[i, indx] * 2
                        point += tmp[i, ind0]
                        ind0 += 1

                        indx += 2
                    else:
                        tmp[i, ind0] = tmp[i, indx]
                        ind0 += 1
                        indx += 1'''
                        


    '''    def left(self):
        tmp = self.board.copy()
        for i in xrange(self.a):
            line = tmp[i, :]
            non_zero = line[line!=0]
            ind = 0
            while ind+1 < len(non_zero):
                if non_zero[ind] == non_zero[ind+1]:
                    non_zero[ind] *= 2
                    non_zero[ind+1] = 0
                    ind += 2
                else:
                    ind += 1
            non_zero = non_zero[non_zero != 0]                    
            line = zeros((self.a))
            line[:len(non_zero)] = non_zero
            tmp[i, :] = line
        return tmp

    def right(self):
        tmp = self.board.copy()
        for i in xrange(self.a):
            line = tmp[i, :][::-1]
            non_zero = line[line!=0]
            ind = 0
            while ind+1 < len(non_zero):
                if non_zero[ind] == non_zero[ind+1]:
                    non_zero[ind] *= 2
                    non_zero[ind+1] = 0
                    ind += 2
                else:
                    ind += 1 
            non_zero = non_zero[non_zero != 0]                    
            line = zeros((self.a))
            line[:len(non_zero)] = non_zero
            tmp[i, :] = line[::-1]
        return tmp

    def up(self):
        tmp = self.board.copy()
        for i in xrange(self.a):
            line = tmp[:, i].T
            non_zero = line[line!=0]
            ind = 0
            while ind+1 < len(non_zero):
                if non_zero[ind] == non_zero[ind+1]:
                    non_zero[ind] *= 2
                    non_zero[ind+1] = 0
                    ind += 2
                else:
                    ind += 1
            non_zero = non_zero[non_zero != 0]                    
            line = zeros((self.a))
            line[:len(non_zero)] = non_zero
            tmp[:, i] = line.T
        return tmp

    def down(self):
        tmp = self.board.copy()
        for i in xrange(self.a):
            line = tmp[:, i][::-1].T
            non_zero = line[line!=0]
            ind = 0
            while ind+1 < len(non_zero):
                if non_zero[ind] == non_zero[ind+1]:
                    non_zero[ind] *= 2
                    non_zero[ind+1] = 0
                    ind += 2
                else:
                    ind += 1
            non_zero = non_zero[non_zero != 0]                    
            line = zeros((self.a))
            line[:len(non_zero)] = non_zero
            tmp[:, i] = line[::-1].T
        return tmp'''


    def __init__(self, a = 4):
        pygame.init()

        self.screen = pygame.display.set_mode((700, 700), 0, 32)       
        self.block_a = 700 / (1.13 * a + 0.13)
        self.margin = self.block_a * 0.13

        self.a = a
        self.block = self.create_digitals()
        pygame.event.set_blocked([ACTIVEEVENT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
        
#    background = pygame.image.load('back.jpg').convert()
#    clock = pygame.time.Clock()

        self.board = zeros((a, a))
        self.change()
        self.change()

    def step(self, movement = None):
        global rec_board, rec_move

        if movement == None:
           event = pygame.event.wait()        
        else:
           event = movement
        if event.type == QUIT:
            exit()
        if event.type == KEYUP:
            if event.key == K_LEFT:
                if self.check(self.left):                    
                    rec_board.append(self.board.flatten())
                    rec_move.append(0)
                    self.change()
            elif event.key == K_RIGHT:
                if self.check(self.right):
                    rec_board.append(self.board.flatten())
                    rec_move.append(1)
                    self.change()
            elif event.key == K_UP:
                if self.check(self.up):
                    rec_board.append(self.board.flatten())
                    rec_move.append(2)
                    self.change()
            elif event.key == K_DOWN:
                if self.check(self.down):
                    rec_board.append(self.board.flatten())
                    rec_move.append(3)
                    self.change()
            elif event.key == K_r:
                self.board = zeros((self.a, self.a))
                print rec_board, rec_move
                self.change()
                self.change()                           
            elif event.key == K_s:
                print rec_board, rec_move
                save('rec_board', rec_board)
                save('rec_move', rec_move)
                rec_board = []
                rec_move = []
   
if __name__ == '__main__':    

#    try:
#        record_f = open(sys.argv[1], 'w')
#    except:
#        record_f = None

    cl = _2048(a = 4) 
    move_up = pygame.event.Event(KEYUP, key=K_UP, mod=0)
    move_right = pygame.event.Event(KEYUP, key=K_RIGHT, mod=0)
    move_down = pygame.event.Event(KEYUP, key=K_DOWN, mod=0)
    move_left = pygame.event.Event(KEYUP, key=K_LEFT, mod=0)

    while True:
        cl.step()

'''    iteration = 0
    while True:
        iteration += 1
#        if sum(cl.board == 0) < 3:
#            cl.step()
#            continue
        if cl.check(cl.up) or cl.check(cl.right) or cl.check(cl.down):
            if random.rand() > 0.50:
                cl.step(move_up)     
                cl.step(move_right)
            else:            
                cl.step(move_right)     
                cl.step(move_up)
            if iteration > 500 and random.rand() > 0.75:
                if cl.board[0, 3] != cl.board.max():
                    cl.step(move_down)
#                cl.step(move_up) 
#        elif cl.check(cl.down):                
#            cl.step(move_down)
#            cl.step(move_up)
        else:
            cl.step(move_left)
            cl.step(move_down)
            cl.step(move_right)
            if not cl.check(cl.left):
                cl.step()'''\
