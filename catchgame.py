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
font=pg.font.SysFont('Impact',52)
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
                        hsv_to_rgb(cot/level,0.5,100),
                        pg.Rect(self.x-self.diag/2,self.y-self.diag/2,self.diag,self.diag),
                        math.tau*cot/level+self.angle,
                        math.tau*(cot+1)/level+self.angle,
                        int(self.diag/8))
            pg.draw.arc(f,
                        hsv_to_rgb(cot/level,0.5,255),
                        pg.Rect(self.x-self.diag/2,self.y-self.diag/2,self.diag,self.diag),
                        math.tau*cot/level+self.angle,
                        math.tau*(cot+1)/level+self.angle,
                        int(self.diag/16))

class Missile:
    def __init__(self):
        self.attack=random.random()*math.tau
        self.x,self.y=(-math.cos(self.attack)+1)*WIND/2,(1-math.sin(self.attack))*WIND/2
        self.teinte=int(random.random()*level)/level
        self.coul=hsv(self.teinte,0.5,255)
        self.dir=(math.cos(self.attack),math.sin(self.attack))
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
    def mouve(self):
        self.x+=self.dir[0]
        self.y+=self.dir[1]
    def test_good(self):
        self.val=math.atan2((WIND/2-self.y),(self.x-WIND/2))-forme.angle
        if self.val<0:self.val+=math.tau
        self.val=self.val%math.tau
        return int(self.val/math.tau*level)/level==self.teinte
b = 1
forme=Carre()
mouv=10
wow=[]
score=0
IsPause=False
dificulty=3
try:
    pg.mixer.music.load("chill.wav")
    pg.mixer.music.set_volume(1)
    pg.mixer.music.play(-1) 
    while b:
        if not IsPause:
            b+=1
        # Actualiser:
        pg.display.flip()
        # Appliquer les images de fond sur la fenetre
        f.fill(0)
        
        forme.draw()
        si = pg.key.get_pressed()  # SI la touche est appuyée
        if not IsPause:
            if si[pg.K_RIGHT]:forme.angle-=math.pi/64
            if si[pg.K_LEFT]:forme.angle+=math.pi/64
        if si[pg.K_a]:wow.append(Missile())
        next_wow=[]
        for i in wow:
            if IsPause==False:i.mouve()
            i.draw()
            if 0<i.x<WIND and 0<i.y<WIND and dist(i,forme)>forme.diag/2:
                next_wow.append(i)
            elif dist(i,forme)<forme.diag/2:
                pg.mixer.Sound("switch.mp3").play()
                if i.test_good():
                    score+=1
                else:
                    score-=1
            
        wow=next_wow[:]
        if not b%100:
            wow.append(Missile())
        for event in pg.event.get():  # QUAND la touche est appuyée
            if event.type == pg.QUIT:
                b = False
                print(" Fin du jeu  babe")
            elif event.type == pg.KEYUP:
                key=event.dict['key']
                if event.key==pg.K_SPACE:
                    IsPause= not IsPause
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
        if int(score/10)+3!=level:
            level=int(score/10)+3
            wow=[]
            pg.mixer.Sound("strike.mp3").play()
      
        s_core=font.render(str(score),1,(255,255,255))
        s_core_rect=s_core.get_rect()
        f.blit(s_core,(WIND/2-s_core_rect.width/2,WIND/2-s_core_rect.height/2))
        if IsPause:
            f.blit(font.render("Pause",1,(255,255,255)),(0,0))


        fpsClock.tick(FPS)
except :
    pg.quit()
    raise
finally:
    pg.quit()
