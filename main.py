import pygame 
from pygame.locals import *
from pygame.sprite import Group
import random



pygame.init()

clock=pygame.time.Clock()
fps=60


screen_width=800
screen_height=720

screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('flappy birb')

font=pygame.font.SysFont('Bauhaus 93',60)
white=(255,255,255)

grnd_scroll=0
scroll_speed=4
flying=False
gameover=False
pipe_gap=150
pipe_freq=1500
last_pipe=pygame.time.get_ticks() - pipe_freq
score=0
passed=False


def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))

def reset():
    pipe_group.empty()
    the_choosen_one.rect.x=100
    the_choosen_one.rect.y=screen_height/2
    return 0

class res:
    def __init__(self,x,y,image):
        self.image=restart
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
    def button(self):
        action =False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                action =True
        screen.blit(self.image,(self.rect.x, self.rect.y))
        return action

class birb(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.count=0
        for i in range(1,4):
            img=pygame.image.load(f'bird{i}.png')
            self.images.append(img)
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.vel=0

    def update(self):

        if flying == True:
            self.vel+=0.5
            if self.vel>8:
                self.vel=8
            if self.rect.bottom<700:
                self.rect.y+=int(self.vel)

        if gameover == False:
            #jump
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                self.vel=-10
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked=False

            self.count+=1
            count_lim=5

            if self.count >count_lim:
                self.count=0
                self.index+=1
                if self.index>=len(self.images):
                    self.index=0
            self.image=self.images[self.index]
            self.image=pygame.transform.rotate(self.images[self.index],self.vel*-2)



class pipe(pygame.sprite.Sprite):
    
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('pipe.png')
        self.rect=self.image.get_rect()
        if position==1:
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=[x,y-int(pipe_gap/2)]
        if position ==-1:
            self.rect.topleft=[x,y+int(pipe_gap/2)]

    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right<0:
            self.kill()

    
brib_group=pygame.sprite.Group()
pipe_group=pygame.sprite.Group()

the_choosen_one=birb(100,100)
restart=pygame.image.load('restart.png')
res_inst=res(screen_width/2 - 50,screen_height/2-100,restart)

brib_group.add(the_choosen_one)


bg=pygame.image.load('bg.png')
ground_img=pygame.image.load('ground.png')



run=True
while(run):

    clock.tick(fps)
    screen.blit(bg,(0,0))
    brib_group.draw(screen)
    brib_group.update()
    pipe_group.draw(screen)
    screen.blit(ground_img,(grnd_scroll,700))


    if len(pipe_group)>0:
        if brib_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left and brib_group.sprites()[0].rect.right<pipe_group.sprites()[0].rect.right and passed == False:
            passed=True
        if passed ==True:
            if brib_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.right:
                score+=1
                passed= False
    draw_text(str(score),font,white,screen_width/2,20)


    if pygame.sprite.groupcollide(brib_group,pipe_group,False,False):
        gameover=True   

    if the_choosen_one.rect.bottom >=700:
        gameover = True
            

    if gameover == False and flying == True:

        time_now=pygame.time.get_ticks()
        if time_now - last_pipe >pipe_freq:
            pipe_randomness=random.randint(-100,100)
            bottom_pipe=pipe(screen_width,int(screen_height/2)+pipe_randomness,-1)
            top_pipe=pipe(screen_width,int(screen_height/2)+pipe_randomness,1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe=time_now

        grnd_scroll-=scroll_speed
        if abs(grnd_scroll)>35: 
            grnd_scroll=0
        pipe_group.update()

    if gameover== True:
        if res_inst.button() == True:
            gameover=False
            score=reset()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False
        if event.type==MOUSEBUTTONDOWN and flying == False and gameover==False:
            flying = True
        
    pygame.display.update()

pygame.quit()