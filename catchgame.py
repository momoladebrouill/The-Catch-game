import pygame as pg

import math
import random
from colorsys import hsv_to_rgb

hsv=hsv_to_rgb
dist=lambda a,b:math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)

class Carre:
    def __init__(self):
        self.x=WIND/2
        self.y=WIND/2
        self.diag=200
        self.angle=0
        self.nbs=level
    def draw(self):
        for cot in range(level):
            nb=2
            for i in range(nb):
                pg.draw.arc(f,
                            hsv_to_rgb(cot/level,0.5,(i+1)/nb*255),
                            pg.Rect(self.x-self.diag/2,self.y-self.diag/2,self.diag,self.diag),
                            math.tau*cot/level+self.angle,
                            math.tau*(cot+1)/level+self.angle,
                            int(self.diag/2**(3+i)))

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
        
        for j in range(1,level+1):
            i=j*math.tau/level+math.pi/2
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
FPS = 60
WIND = 750
level=3
forme=Carre()
wow=[]
score=0
IsPause=False
si={}

try:
    pg.init()
    f = pg.display.set_mode((WIND, WIND))
    pg.display.set_caption("THE TRIGONOMETRISATOR")
    fpsClock = pg.time.Clock()
    font=pg.font.SysFont('Impact',52)
    sub_font=pg.font.SysFont('Impact',26)
    pg.mixer.music.load("chill.wav")
    pg.mixer.music.play(-1)
    forme.y=200
    forme.draw()

    title=font.render('The Trigonometrisator',1,(100,100,100))
    titlerect=title.get_rect()
    f.blit(title,(WIND/2-titlerect.width/2+5,WIND/2-titlerect.height/2+5))
    
    title=font.render('The Trigonometrisator',1,(255,255,255))
    f.blit(title,(WIND/2-titlerect.width/2,WIND/2-titlerect.height/2))
    decal=WIND/2+titlerect.height/2
    
    arrow=sub_font.render('Flèches de gauche et de droite pour tourner le disque',1,(200,200,200))
    arrowrect=arrow.get_rect()
    f.blit(arrow,(WIND/2-arrowrect.width/2,decal))
    decal+=arrowrect.height

    arrow=sub_font.render('Presser A pour faire le gue-din',1,(200,200,200))
    arrowrect=arrow.get_rect()
    f.blit(arrow,(WIND/2-arrowrect.width/2,decal))
    decal+=arrowrect.height
    
    space=sub_font.render('Barre espace pour une pause ou lancer le JEUVIDEOGAMING',1,(200,200,200))
    f.blit(space,(WIND/2-space.get_rect().width/2,decal))
    
    pg.display.flip()
    affecter=0
    while b:
        pg.display.flip()
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                raise IndexError
            elif event.type==pg.KEYDOWN:
                if event.key==pg.K_SPACE:
                    b=0
                elif event.key==pg.K_RIGHT:
                    affecter=math.pi/64
                elif event.key==pg.K_LEFT:
                    affecter=-math.pi/64
                else:
                    affecter=0
            elif event.type==pg.KEYUP:
                affecter=0
        if affecter:
            forme.angle+=affecter/10
            forme.draw()
    b=1
    forme.y=WIND/2
    while b:
        if not IsPause:
            b+=1
            
        pg.display.flip()
        f.fill(0)
        forme.draw()
        if not IsPause:
            if si.get(pg.K_RIGHT):forme.angle-=math.pi/64
            if si.get(pg.K_LEFT):forme.angle+=math.pi/64
        
        next_wow=[]
        for i in wow:
            if not IsPause:i.mouve()
            i.draw()
            if dist(i,forme)>forme.diag/2:
                next_wow.append(i)
            elif dist(i,forme)<forme.diag/2:
                pg.mixer.Sound("switch.mp3").play()
                if i.test_good():score+=1
                else:score-=1
                
        wow=next_wow[:]
        
        if not b%100:wow.append(Missile())
        
        for event in pg.event.get(): 
            if event.type == pg.QUIT:
                b = False
                print(" Fin du jeu  babe")
            elif event.type == pg.KEYDOWN:
                si[event.dict.get('key',' ')]=True
                if event.key==pg.K_SPACE:
                    IsPause= not IsPause
                if event.key==pg.K_ESCAPE:
                    forme.angle=0
            elif event.type==pg.KEYUP:
                si[event.dict.get('key',' ')]=False
            elif event.type == pg.MOUSEBUTTONUP:
                
                if event.button==1: #click gauche
                    forme.nbs+=1
                if event.button==3: #click droit"""
                    forme.nbs-=1
                if event.button==4: 
                    forme.diag+=10
                elif event.button==5: 
                    forme.diag-=10
        if int(score/10)+3!=level:
            level=int(score/10)+3
            wow=[]
            pg.mixer.Sound("strike.mp3").play()
        if si.get(pg.K_a):wow.append(Missile())

        s_core=font.render(str(score),1,(255,255,255))
        s_core_rect=s_core.get_rect()
        f.blit(font.render(str(score),1,(100,100,100)),(WIND/2-s_core_rect.width/2+5,WIND/2-s_core_rect.height/2+5))
        f.blit(s_core,(WIND/2-s_core_rect.width/2,WIND/2-s_core_rect.height/2))
        
        if IsPause:
            f.blit(font.render("Pause-in",1,(255,255,255)),(0,0))
            f.blit(sub_font.render("Allez hop E prépausal dans ta geule",1,(100,100,100)),(0,50))


        fpsClock.tick(FPS)
except :
    pg.quit()
    raise
finally:
    pg.quit()
