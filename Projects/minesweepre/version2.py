#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Synopsis: A pygame based Microsoft Windows Minesweeper like game
Filename: minefield.py
Author: zhaoxin
Date: 2011/03/26
Website: http://imzhao.net:8008/~zhaoxin/
Mail: archtaurus@gmail.com
'''
import pygame
from pygame.locals import *
#from os import path
from random import shuffle
from time import sleep, time
from sys import exit
pygame.init() #初始化pygame
pygame.mixer.init()
imgpath = "./images/" #设定图目录位置并载入图片
sndpath = "./sounds/"
image = {\
0: pygame.image.load(imgpath+'0.png'),
1: pygame.image.load(imgpath+'1.png'),
2: pygame.image.load(imgpath+'2.png'),
3: pygame.image.load(imgpath+'3.png'),
4: pygame.image.load(imgpath+'4.png'),
5: pygame.image.load(imgpath+'5.png'),
6: pygame.image.load(imgpath+'6.png'),
7: pygame.image.load(imgpath+'7.png'),
8: pygame.image.load(imgpath+'8.png'),
"mine": pygame.image.load(imgpath + 'mine.png'),
"field": pygame.image.load(imgpath + 'field.png'),
"flag": pygame.image.load(imgpath + 'flag.png'),
"wrong": pygame.image.load(imgpath + 'wrong.png'),
"boom": pygame.image.load(imgpath + 'boom.png'),
"mouse": pygame.image.load(imgpath + 'sweeper.png')}
sound = {
"boom": pygame.mixer.Sound(sndpath+'boom.wav'),
"dig": pygame.mixer.Sound(sndpath+'dig.wav'),
"flag": pygame.mixer.Sound(sndpath+'flag.wav'),
"win": pygame.mixer.Sound(sndpath+'win.wav'),
"loss": pygame.mixer.Sound(sndpath+'loss.wav')}
pygame.mixer.music.load(sndpath+'bgmusic.wav')

#设定一些全局变量
fieldWidth, fieldHeight = 96, 54 #64, 36
sumFields, tileSize = fieldWidth * fieldHeight, 20
sumMines = sumFields / 10
sumLands, sumDigged = fieldWidth * fieldHeight - sumMines, 0
#设定显示属性并创建显示窗口
winWidth, winHeight = tileSize * fieldWidth, tileSize * fieldHeight
appname = "Minefield"
screen = pygame.display.set_caption(appname)
pygame.display.set_icon(image["mine"])
screen = pygame.display.set_mode((winWidth, winHeight))
font = pygame.font.Font('freesansbold.ttf', 16)



class Field(object): #定义地块对象类
                          
    def __init__(self, ismine = 0):
        self.ismine = ismine
        self.digged = False
        self.flagged = False
        self.image = image["field"]
        self.neighbours = []
        self.minesnearby = 0
        self.x = self.y = 0
                          
    def Draw(self, img = "field"):
        global tileSize
        self.flagged = img == "flag"
        if img != "self":
            self.image = image[img]
        else:
            pass
        screen.blit(self.image, (self.x, self.y))
        #用update方法比满屏幕更新方法pygame.display.flip()效率高不少
        pygame.display.update((self.x, self.y, self.x + tileSize, self.y + tileSize))
                          
    def Clicked(self, button):
        if button == 1:
            if self.digged and self.minesnearby != 0:
                self.Autodig()
            else:
                return self.Dig()
        elif button == 3 and not self.digged:
            if self.flagged:
                self.Draw("field")
            else:
                self.Draw("flag")
                sound["flag"].play()
                          
    def Dig(self):
        global sumLands, sumDigged
        if not self.flagged and not self.digged:
            self.digged = True
            if self.ismine:
                self.Draw("boom")
                sound["boom"].play()
            else:
                sumDigged += 1
                sound["dig"].play()
                #print sumLands - sumDigged
                self.Draw(self.minesnearby)
                if self.minesnearby == 0:
                    self.Autodig()
                          
    def Autodig(self):
        flags = 0
        for field in self.neighbours:
            if field.flagged:
                flags += 1
        if flags == self.minesnearby:
            for field in self.neighbours:
                field.Dig()
                          
                          
class Minefield(object): #定义雷场对象类
                          
    def __init__(self):
        global sumDigged
        sumDigged = 0
        self.startTime = time()          #设定游戏开始时间
        self.fields, self.mines = [], [] #初始化地块列表及地雷列表
        for i in range(sumMines):        #创建sumMines块地雷地块
            self.fields.append(Field(1)) #将地雷地块放入地块列表
        for field in self.fields:
            self.mines.append(field)     #将地雷地块放入地雷列表
        for i in range(sumLands):
            self.fields.append(Field())  #创建其它地块并放入地块列表
        shuffle(self.fields)             #打乱地块列表的排序
        for n in range(sumFields):       #设定所有地块的邻居列表及周边雷数
            if n % fieldWidth == 0:
                for i in [n+1, n-fieldWidth, n-fieldWidth+1, n+fieldWidth, n+fieldWidth+1]:
                    if i in range(sumFields):
                        self.fields[n].neighbours.append(self.fields[i])
                        self.fields[n].minesnearby += self.fields[i].ismine
            elif n % fieldWidth == fieldWidth-1:
                for i in [n-1, n-fieldWidth-1, n-fieldWidth, n+fieldWidth-1, n+fieldWidth]:
                    if i in range(fieldWidth * fieldHeight):
                        self.fields[n].neighbours.append(self.fields[i])
                        self.fields[n].minesnearby += self.fields[i].ismine
            else:
                for i in [n+1, n-1, n-fieldWidth-1, n-fieldWidth, n-fieldWidth+1, n+fieldWidth-1, n+fieldWidth, n+fieldWidth+1]:
                    if i in range(fieldWidth * fieldHeight):
                        self.fields[n].neighbours.append(self.fields[i])
                        self.fields[n].minesnearby += self.fields[i].ismine
        for y in range(fieldHeight):    #初始化所有地块的位置并在屏幕上绘制
            for x in range(fieldWidth):
                n = y*fieldWidth+x
                px, py = tileSize*x, tileSize*y
                self.fields[n].x = px
                self.fields[n].y = py
                screen.blit(image["field"], (px, py))
        pygame.display.flip()
        pygame.mixer.music.play(-1)
                          
    def Clicked(self, x, y, button):
        #将点击传递给相应地块, 若得到的反应居然是"boom"的一声, 则不解释了......
        self.fields[(x/tileSize) + fieldWidth * (y/tileSize)].Clicked(button)
        for mine in self.mines:
            if mine.digged:
                self.Loss()
        #若所有空地都挖干净了, 则成功了!
        if sumDigged == sumLands:
            self.Win()
                          
    def Win(self): #赢了,如何?
        pygame.mixer.music.stop()
        sound["win"].play()
        self.gameTime = time() - self.startTime
        for mine in self.mines: #给所有地雷插上小旗子
            mine.Draw("flag")
        #恭喜玩家,提示所用时间,选择再玩一次或者退出
        #print "Congratulations! You did it in", self.gameTime, "seconds." ##有待更新##
        self.ShowText(" Congratulations! You did it in %.1f seconds. Click to play again... " % self.gameTime)
        self.Reset()
                          
    def Loss(self): #输了,又如何?
        pygame.mixer.music.stop()
        sleep(1)
        sound["loss"].play()
        for field in self.fields:
            #显示没有找到的雷
            if field.ismine and field.image != image["boom"] and not field.flagged:
                field.Draw("mine")
            #显示误判的雷
            elif field.flagged and not field.ismine:
                field.Draw("wrong")
        #鼓励玩家,选择再玩一次或者退出
        #print "You are sure to make it in next time!" ##有待更新##
        self.ShowText(" You\'re sure to make it in next time! Click to try again... ")
        self.Reset()
                          
    def ShowText(self, msg, pos = screen.get_rect().center):
        text = font.render(msg, True, (255, 0, 0), (255, 255, 255))
        textpos = text.get_rect()
        textpos.center = pos
        screen.blit(text, textpos, special_flags = 0)
        pygame.display.flip()
                          
    def Reset(self):
        while True:
            sleep(0.01)
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.type != pygame.QUIT:
                    self.__init__()
                    return
                elif event.type == pygame.QUIT:
                    exit()
                          
Game = Minefield() #启动游戏, 创建一个Minefield
fullscreen = False
                          
while True: #程序主循环
    sleep(0.01) #为了减少CPU占用和可持续发展, 每0.01秒探测一次用户输入, 然后就睡觉(休息, 休息一下)
    #x, y = pygame.mouse.get_pos()
    #screen.blit(image["mouse"], (x, y))
    #pygame.display.flip()
    for event in pygame.event.get(): #探测所有用户输入事件
        if event.type == pygame.QUIT: #如果关闭窗口则程序结束
            Game.running = False
            pygame.quit()
            exit()
            #raise SystemExit
        elif event.type == MOUSEBUTTONDOWN: #如果点击鼠标则将点击信息传递给游戏
            Game.Clicked(event.pos[0], event.pos[1], event.button)
        elif event.type == KEYDOWN:
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((winWidth, winHeight), FULLSCREEN|HWSURFACE, 32)
                else:
                    screen = pygame.display.set_mode((winWidth, winHeight), 0, 32)
                for field in Game.fields:
                    #field.Draw("self")
                    screen.blit(field.image, (field.x, field.y))
                pygame.display.flip()
        else: #其它用户输入接口预留位置
            pass
