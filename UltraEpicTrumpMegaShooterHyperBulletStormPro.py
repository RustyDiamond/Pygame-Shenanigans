import pygame
import random
import time
pygame.init()
pygame.font.init()

blue=(0,0,255)
red=(255,0,0)

Count=''
countnum=0
Hit=''
hitcount=0


screen = pygame.display.set_mode((600,600))
clock=pygame.time.Clock()


start_time=starttt=bullet_start=wavetime=time.monotonic()
end_time=0
enddd=0
bullet_time=0
hit=0
spawn=0.2
donnie=pygame.image.load("donnie.png")
print(donnie.get_width())
print(donnie.get_height())
xp=270
halfx=xp+(donnie.get_width()/2)
yp=300
halfy=yp+(donnie.get_height()/2)


objs=[]
bullets=[]
pos=-1
bullet_count=-1
wavecount=1

n=1
jump=False
vel=3
jumpheight=0
n=1

face="RIGHT"
bullet=[]


def game():
    
    clock.tick()
    
    screen.fill((255,255,255))
    global check_time,end_time,enddd,bullet_time,start_time,starttt,bullet_start,xp,yp,Count,Hit\
    ,pos,countnum,hitcount,halfx,halfy,player_rect,obj_rect,bullet_count,bullet_rect,waveend,wavetime,\
    wavecount,spawn

    
    check_time=time.monotonic()
    end_time=check_time-start_time
    enddd=check_time-starttt
    bullet_time=check_time- bullet_start
    waveend=check_time-wavetime
    
    for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    jump=True
            
    keys=pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        
        xp+=2
        halfx=xp+(donnie.get_width()/2)
    elif keys[pygame.K_LEFT]:
        
        xp-=2
        halfx=xp+(donnie.get_width()/2)
    
    if keys[pygame.K_UP] :
        yp-=2
        halfy=yp+(donnie.get_height()/2)
    elif keys[pygame.K_DOWN]:
        yp+=2
        halfy=yp+(donnie.get_height()/2)
    if keys[pygame.K_d] and bullet_time>0.5:
        face="RIGHT"
        bullet_rect=pygame.Rect(player_rect.x+90,player_rect.y+(donnie.get_height()/2),20,20)
        bullet=[bullet_rect,face]
        if bullet:
            bullets.append(bullet)
        bullet_start=time.monotonic()
    elif keys[pygame.K_a] and bullet_time>0.5:
        face="LEFT"
        bullet_rect=pygame.Rect(player_rect.x-10,player_rect.y+(donnie.get_height()/2),20,20)
        bullet=[bullet_rect,face]
        if bullet:
            bullets.append(bullet)
        bullet_start=time.monotonic()

    if yp+110>600:
        yp=600-110
    elif yp<0:
        yp=0

    if xp<0:
        xp=0
    elif xp+89>600:
        xp=600-89

    if enddd>1:
        countnum+=1
        Count=str(countnum)
        starttt=time.monotonic()

    if waveend>11:
        wavecount+=1
        spawn-=0.02
        wavetime=time.monotonic()

    if end_time>spawn:

        red=random.randint(0,255)
        green=random.randint(0,255)
        blue=random.randint(0,255)
        colour=(red,green,blue)
        xo=random.randint(-20,620)
        yo=random.randint(-20,620)
        if xo+10<0 or xo>600 or yo+10<0 or yo>600 :
            objs.append([xo,yo,colour])
        start_time=time.monotonic()
        
      
    player_rect=pygame.Rect(xp,yp,89,110)
    screen.blit(donnie,(player_rect.x,player_rect.y))

    pos=-1
    if len(objs)>0:
        for k in objs:
            
            pos+=1
            

            dist=((halfx-k[0])**2+(halfy-k[1])**2)**0.5

            k[0]+=(halfx-k[0])/(dist*1)*n
            k[1]+=(halfy-k[1])/(dist*1)*n
            
            

            obj_rect=pygame.Rect(k[0],k[1],20,20)
            
            pygame.draw.rect(screen,k[2],obj_rect)

            if player_rect.colliderect(obj_rect):

                hitcount+=1
                Hit=str(hitcount)
               
                objs.pop(pos)
               
    pos=-1
    if bullets:      
        for bullet in bullets:
            bullet_count+=1
            if bullet[1]=="LEFT":
                bullet[0].x-=4
                if bullet[0].x>600:
                    bullets.pop(bullet_count)
            else:
                bullet[0].x+=4
                if bullet[0].x+10<0:
                    bullets.pop(bullet_count)
            
            pygame.draw.rect(screen,(255,0,0),bullet[0])
            for k in objs:
                pos+=1
                box=pygame.Rect(k[0],k[1],20,20)
                
                

                if bullet[0].colliderect(box):
                    objs.pop(pos)

            pos=-1
        bullet_count=-1


    pos=-1
    myfont = pygame.font.SysFont('Comic Sans MS', 70)
    textsurface = myfont.render(Count, False, (0, 0, 0))
    wavesurface = myfont.render("Wave "+str(wavecount), False, (0, 0, 0))
    hitsurface = myfont.render(Hit, False, (0, 0, 0))
    
    screen.blit(textsurface,(0,0))
    screen.blit(wavesurface,(200,0))
    screen.blit(hitsurface,(0,500))
    clock.tick(120)
    pygame.display.update()
while True:
    game()
    if hitcount>=10:
            break

myfont = pygame.font.SysFont('Comic Sans MS', 70)
textsurface = myfont.render(Count, False, (0, 0, 0))  

secs= myfont.render("secs", False, (0, 0, 0)) 
while True:
    screen.fill((255,255,255))
    for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
     
    screen.blit(textsurface,(220,240))
    xco=(textsurface.get_width())
    screen.blit(secs,(220+xco,240))
    pygame.display.update()    
