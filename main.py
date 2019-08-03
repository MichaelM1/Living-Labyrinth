import sys, pygame
import os
pygame.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Living Labyrinth")
walkRight = [pygame.image.load('left1.png'), pygame.image.load('left2.png'), 
pygame.image.load('left3.png'), pygame.image.load('left4.png'), ]
walkLeft = [pygame.image.load('left1.png'), pygame.image.load('left2.png'), 
pygame.image.load('left3.png'), pygame.image.load('left4.png'), ]
clock = pygame.time.Clock()
bg = pygame.image.load('a.png')

class Player(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.spriteAnim = 0
    def draw(self, win):
        if self.left:  
            win.blit(walkLeft[self.spriteAnim%3], (self.x,self.y))    
            self.spriteAnim+=1                    
        elif self.right:
            win.blit(walkRight[self.spriteAnim%3], (self.x,self.y))
            self.spriteAnim+=1 

class Movable(object):
    def __init__(self,z,a):
        self.z = z
        self.a = a
        self.left = False
        self.right = False
        self.up = False
        self.down = False
    def drawMove(self, win):
        if self.left:
            win.blit(bg,(self.z,self.a))
        elif self.right:
            win.blit(bg,(self.z,self.a))
        elif self.up:
            win.blit(bg,(self.z,self.a))

def redrawGameWindow():
    map.drawMove(win)
    ball.draw(win)
    pygame.display.update()

ball = Player(150,150)
map = Movable(0,0)
run = True
while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: 
        ball.left = True
        map.left = True
        map.z+=10
    elif keys[pygame.K_RIGHT]:  
        ball.right = True
        map.right = True
        map.z-=10
    elif keys[pygame.K_UP]:
        map.up = True
        map.a+=10
    elif keys[pygame.K_DOWN]:
        map.down = True
        map.a-=10
    else: 
        ball.spriteAnim = 0
    win.fill((0,0,0))
    redrawGameWindow()

pygame.quit()