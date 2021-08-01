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
    def __init__(self,x=WIND/2,y=WIND/2,cote=200):
        self.x=x
        self.y=y
        self.diag=cote
        self.angle=0
        self.nbs=level
    def draw(self):
        for cot in range(level):
            pg.draw.arc(f,
                        hsv_to_rgb(cot/level,1,255),
                        pg.Rect(self.x-self.diag/2,self.y-self.diag/2,self.diag,self.diag),
                        math.tau*cot/level+self.angle,
                        math.tau*(cot+1)/level+self.angle,
                        int(self.diag/4))

class Missile:
    def __init__(self):
        self.attack=random.random()*math.tau
        self.x,self.y=(-math.cos(self.attack)+1)*WIND/2,(1-math.sin(self.attack))*WIND/2
        
        self.coul=hsv(int(random.random()*level)/level,1,255)
        self.dir=(math.cos(self.attack),math.sin(self.attack))
        self.angle=0
    def draw(self):
        points=[]
        self.coul=self.test_good()
        self.angle+=0.1
        self.angle=self.angle%math.tau
        for j in range(1,4):
            i=j*math.tau/3+math.pi/2
            points.append((self.x+math.cos(self.angle+i)*10,
                           self.y+math.sin(self.angle+i)*10))
        pg.draw.polygon(f,self.coul,points)
        self.x+=self.dir[0]
        self.y+=self.dir[1]
    def test_good(self):
        self.val=math.atan2((WIND/2-self.y),(self.x-WIND/2))-forme.angle
        if self.val<0:self.val+=math.tau
        self.val=self.val%math.tau
        return hsv((int(self.val/math.tau*level))/level,1,255)
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
        f.fill(0)
        
        forme.draw()
        si = pg.key.get_pressed()  # SI la touche est appuyée
       
        if si[pg.K_RIGHT]:forme.angle-=math.pi/64
        if si[pg.K_LEFT]:forme.angle+=math.pi/64
        if si[pg.K_a]:wow.append(Missile())
        next_wow=[]
        for i in wow:
            i.draw()
            if 0<i.x<WIND and 0<i.y<WIND and dist(i,forme)>forme.diag/2:
                next_wow.append(i)
            elif dist(i,forme)<forme.diag/2:
                i.__init__()
                next_wow.append(i)
            
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
                    
                    level+=1
                if key==pg.K_DOWN:
                  
                    level-=1
                    level=abs(level-1)+1
                if key==pg.K_ESCAPE:
                    forme.angle=0
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button==1: #click gauche
                    forme.nbs+=1
                if event.button==3: #click droit"""
                    forme.nbs-=1
                if event.button==4: #vers le haut
                    forme.diag+=10
                elif event.button==5: #vers le bas
                    forme.diag-=10



        fpsClock.tick(FPS)
except :
    pg.quit()
    raise
finally:
    pg.quit()
