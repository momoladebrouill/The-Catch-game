import pygame as pg

import math
import random
from colorsys import hsv_to_rgb
hsv=hsv_to_rgb
# Constantes :
FPS = 60  # les fps tabernak
WIND = 750 # dimentions de la fentere
pg.init()
f = pg.display.set_mode(size=(WIND, WIND))
pg.display.set_caption("")
fpsClock = pg.time.Clock()
font=pg.font.SysFont('consolas',52)
level=3
dist=lambda a,b:math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)
class Pos:
    def __init__(self,x=WIND/2,y=WIND/2):
        self.x=x
        self.y=y
class Carre:
    def __init__(self,x=WIND/2,y=WIND/2,cote=100):
        self.x=x
        self.y=y
        self.cote=cote
        self.angle=0
        self.nbs=4
    def draw(self):
        
        points=[]
        for j in range(1,self.nbs+1):
            i=j*math.tau/self.nbs+math.pi/2
            points.append((self.x+math.cos(self.angle+i)*self.cote,
                           self.y+math.sin(self.angle+i)*self.cote))
        #pg.draw.polygon(f,(255,255,255),points)
        for i in range(len(points)-1):
            pg.draw.line(f,hsv((i+1)/(len(points)-1),1,255),points[i+1],points[i])
        pg.draw.line(f,hsv(1,1,255),points[0],points[-1])

class Missile:
    def __init__(self):
        self.attack=random.random()*math.tau
        self.x=math.cos(self.attack)*WIND
        self.y=math.sin(self.attack)*WIND
        self.coul=hsv(int(random.random()*level)/level,1,255)
        self.dir=(self.x/self.x*-1,self.y/self.y*-1)
        self.angle=0
    def draw(self):
        points=[]
        self.angle+=0.1
        self.angle=self.angle%math.tau
        for j in range(1,4):
            i=j*math.tau/3+math.pi/2
            points.append((self.x+math.cos(self.angle+i)*10,
                           self.y+math.sin(self.angle+i)*10))
        pg.draw.polygon(f,self.coul,points)
        self.x+=self.dir[0]
        self.y+=self.dir[1]
        
b = 1
forme=Carre()
mouv=10
wow=[]
try:
    while b:
        b+=1
        # Actualiser:
        pg.display.flip()
        # Appliquer les images de fond sur la fenetre
        s = pg.Surface((WIND, WIND))  
        s.set_alpha(360)
        s.fill((0, 0, 0))
        f.blit(s, (0, 0))
        forme.draw()
        si = pg.key.get_pressed()  # SI la touche est appuyée
        if si[pg.K_z]:forme.y-=mouv
        if si[pg.K_q]:forme.x-=mouv
        if si[pg.K_s]:forme.y+=mouv
        if si[pg.K_d]:forme.x+=mouv
        if si[pg.K_RIGHT]:forme.angle+=math.pi/64
        if si[pg.K_LEFT]:forme.angle-=math.pi/64
        if si[pg.K_a]:wow.append(Missile())
        next_wow=[]
        for i in wow:
            i.draw()
            if dist(i,Pos(WIND/2,WIND/2))>forme.cote:
                next_wow.append(i)
            else:
                ouverture=math.tau/level
        wow=next_wow[:]
        if not b%100:
            wow.append(Missile())
        for event in pg.event.get():  # QUAND la touche est appuyée
            if event.type == pg.QUIT:
                b = False
                print(" Fin du jeu  babe")
            elif event.type == pg.KEYUP:
                key=event.dict['key']
                if key==pg.K_UP:
                    forme.nbs+=1
                if key==pg.K_DOWN:
                    forme.nbs-=1
                if key==pg.K_ESCAPE:
                    forme.angle=0
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button==1: #click gauche
                    forme.nbs+=1
                if event.button==3: #click droit"""
                    forme.nbs-=1
                if event.button==4: #vers le haut
                    forme.cote+=10
                elif event.button==5: #vers le bas
                    forme.cote-=10



        fpsClock.tick(FPS)
except :
    pg.quit()
    raise
finally:
    pg.quit()
