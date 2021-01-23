import pygame
import random
import time

pygame.init()

screen=pygame.display.set_mode((600,600))
clock=pygame.time.Clock()
objlist=[]
jump=False
jumpcount=10
bounce=1
shade="SOLID"  #default colour mode
action="ADD"
orient="DOWN"
colours=[(255,255,255),(0,0,0),(150,0,0),(0,150,0),(0,0,120),(50,100,100),(100,50,100),(100,100,50),(50,180,180),\
        (180,50,180),(180,180,50),(100,100,100),(50,50,50),(150,150,150)]
prev=bg=colours[random.randint(0,len(colours))-1]
starttime=time.monotonic()

class Object:
    def __init__(self,xpos,ypos,shade,colour=0,gravity=0,jump=False,jumpcount=10,bounce=1):
        self.gravity=gravity                     ##
        self.colour=colour                        #
        self.shade=shade                          # various values related to
        self.jump=jump                            # each individual sqaure
        self.jumpcount=jumpcount                  #
        self.bounce=bounce                        #
        self.rect=pygame.Rect(xpos,ypos,50,50)   ##

while True:
    clock.tick(60)
    screen.fill(bg)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:       #close window and exit
            pygame.quit()
            exit()

        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:     
                if shade=="SOLID":        #switching square colour modes
                    shade="MULTI"
                else:
                    shade="SOLID"
            elif event.key==pygame.K_RETURN:
                while True:                      #switching bg colours
                    bg=random.choice(colours)
                    if bg==prev:
                        continue
                    prev=bg
                    break
            elif event.key==pygame.K_z:
                if action=="ADD":          #switch scroll func; either add or remove sqrs
                    action="REMOVE"
                else:
                    action="ADD"
            elif event.key==pygame.K_UP:
                orient="UP"
            elif event.key==pygame.K_DOWN:
                orient="DOWN"
            elif event.key==pygame.K_LEFT:
                orient="LEFT"
            elif event.key==pygame.K_RIGHT:
                orient="RIGHT"

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseclick=1
            if event.button==1 or action=="ADD" and event.button==4:    #right click or scroll
                pos=pygame.mouse.get_pos()
                if shade=="SOLID":
                    r=random.randint(0,255)       #random colours
                    g=random.randint(0,255)
                    b=random.randint(0,255)
                    objlist.append(Object(pos[0],pos[1],shade,(r,g,b)))
                else:
                    objlist.append(Object(pos[0],pos[1],shade))

            elif event.button==3 or action=="REMOVE" and event.button==4:    #left click
                if objlist:
                    mx,my=pygame.mouse.get_pos()      #coords of mouse click
                    for obj in range(len(objlist)): 
                        objlist=[obj for obj in objlist if not obj.rect.collidepoint(mx,my)]     #rewrite list, exclude clicked square
                                                                                                 #pop/remove wont work here. 
                                                                                                 #LIST COMP IS A LIFE-SAVER
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:        #empty square list;clear screen
                objlist=[]

    if objlist:                    #iterate through square list if not empty
        for obj in range(len(objlist)):      

            if objlist[obj].rect.x<0:               ##
                objlist[obj].rect.x=0                #
                objlist[obj].gravity=0               #(NTS-not sure if gravity=0 is necessary)
            elif objlist[obj].rect.x+50>600:         #     
                objlist[obj].rect.x=600-50           #
                objlist[obj].gravity=0               #  screen edge boundaries
            if objlist[obj].rect.y<0:                # 
                objlist[obj].rect.y=0                #
                objlist[obj].gravity=0               #
            elif objlist[obj].rect.y+50>600:         # 
                objlist[obj].rect.y=600-50           #
                objlist[obj].gravity=0              ##


            if orient=="DOWN" or orient=="UP":                            ###
                if orient=="DOWN":
                    if objlist[obj].rect.y+50<600:        
                        objlist[obj].rect.y+=objlist[obj].gravity**2/10     #
                elif orient=="UP":
                    if objlist[obj].rect.y>0:        
                        objlist[obj].rect.y-=objlist[obj].gravity**2/10     #

                if objlist[obj].gravity>30:                                 #       #
                    objlist[obj].gravity=30
                else:
                    objlist[obj].gravity+=1                                 #       #    
                                                                                            #orientation specific gravity
            elif orient=="RIGHT" or orient=="LEFT":                         #       #         
                if orient=="RIGHT":
                    if objlist[obj].rect.x+50<600:        
                        objlist[obj].rect.x+=objlist[obj].gravity**2/10     #       #   
                elif orient=="LEFT":
                    if objlist[obj].rect.x>0:        
                        objlist[obj].rect.x-=objlist[obj].gravity**2/10     #     

                if objlist[obj].gravity>30:                                 #
                    objlist[obj].gravity=30
                else:
                    objlist[obj].gravity+=1                               ###


            # if objlist[obj].rect.y+50==600:       #bounce (doesn't work(yet). Uncomment if you want a seizure.)
            #     objlist[obj].jump=True
            #     objlist[obj].bounce=1
            #     objlist[obj].rect.y-=jumpcount**2/bounce

            for obj1 in objlist:
                if objlist[obj]!=obj1 and objlist[obj].rect.colliderect(obj1.rect):  #Top-down collisions;stacking             
                    if orient=="DOWN":
                        if objlist[obj].rect.bottom>obj1.rect.top:
                            objlist[obj].rect.bottom=obj1.rect.top
                            objlist[obj].gravity=0
                        # elif obj1.rect.bottom>objlist[obj].top:    #NTS-not sure if this is necessary;seems to work fine without it
                        #     obj1.rect.bottom=objlist[obj].top
                        #     obj1.gravity=0
                    elif orient=="UP":
                        if objlist[obj].rect.top<obj1.rect.bottom:
                            objlist[obj].rect.top=obj1.rect.bottom
                            objlist[obj].gravity=0
                        # elif obj1.rect.top<objlist[obj].bottom:   # " "
                        #     obj1.rect.top=objlist[obj].bottom
                        #     obj1.gravity=0
                    elif orient=="RIGHT":
                        if objlist[obj].rect.right>obj1.rect.left:
                            objlist[obj].rect.right=obj1.rect.left
                            objlist[obj].gravity=0
                        # elif obj1.rect.right>objlist[obj].left:   # " "
                        #     obj1.rect.right=objlist[obj].left
                        #     obj1.gravity=0
                    elif orient=="LEFT":
                        if objlist[obj].rect.left<obj1.rect.right:
                            objlist[obj].rect.left=obj1.rect.right
                            objlist[obj].gravity=0
                        # elif obj1.rect.left<objlist[obj].right:   # " "
                        #     obj1.rect.left=objlist[obj].right
                        #     obj1.gravity=0

            if objlist[obj].shade=="SOLID":
                pygame.draw.rect(screen,objlist[obj].colour,objlist[obj].rect)
            else:
                r=random.randint(0,255)             #flash through random colours each frame(MULTI)
                g=random.randint(0,255)
                b=random.randint(0,255)
                pygame.draw.rect(screen,(r,g,b),objlist[obj].rect)

    pygame.display.update()






    