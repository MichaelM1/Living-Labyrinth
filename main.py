import sys, pygame
pygame.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Living Labyrinth")
clock = pygame.time.Clock()
background = pygame.image.load('background.jpg').convert()


map = ["WWWWWWWWWWWWWWWWWWWW",
       "WW W WWWWW WWWWW W W",
       "W    W       W   W W",
       "WW WWW W WWW W WWW W",
       "WW                 W",
       "WWWWWW WWW WWW W W W",
       "WW         W W W   W",
       "WWWWWW WWW W W W WWW",
       "WWWW WWW WWW W WWW W",
       "WWWW WWW WWW W WWW W",
       "W    W   W     W W W",
       "WWWWWW WWWWW WWW WWW",
       "W            W     W",
       "WWWWWW WWWWWWWWWWW W",
       "W      W W         W",
       "WWWW WWW W WWW WWW W",
       "WW                 W",
       "WWWWWWWW WWWWWWW W W",
       "W    W           W W",
       "WWWWWWWWWWWWWWWWWWWW"]

class Player(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.player_width  = width = 20
        self.player_height = height = 20
        spritesheet = pygame.image.load('ball.png').convert()
        sprite_list = []
        for sprite in range(9):
            sprite_rect = pygame.Rect(sprite * width, 0, width, height)
            image = pygame.Surface(sprite_rect.size).convert()
            image.blit(spritesheet, (0,0),sprite_rect)
            alpha = image.get_at((0,0))
            image.set_colorkey(alpha)
            sprite_list.append(image)
        self.player_img = sprite_list[0]
        self.player_img_rect = self.player_img.get_rect()
        self.hitbox = (self.x - 10, self.y - 10, width-10,height-10)
    def draw(self, win): 
            win.blit(self.player_img, (self.x,self.y))                        
    def move(self,dx,dy):
        self.x -= dx
        self.y -= dy
        col = False
        for wall in walls:
            if self.x+10>(wall.x + wall.hitbox[2]) or wall.x > (self.hitbox[2] + self.x):
                col = False
            elif self.y+10>(wall.y + wall.hitbox[3]) or wall.y>(self.y + self.hitbox[3]):
                col = False
            else: 
                col = True
                break
        if col:
            self.x +=dx
            self.y +=dy
    
walls = []
walz = pygame.image.load('walla.png')
class Wall(object):
    def __init__(self,pos):
        self.player_width  = width = 25
        self.player_height = height = 25
        w = pygame.image.load('walla.png').convert()
        sprite_rect = pygame.Rect(width, 0, width, height)
        image = pygame.Surface(sprite_rect.size).convert()
        image.blit(w, (0,0),sprite_rect)
        alpha = image.get_at((0,0))
        image.set_colorkey(alpha)
        self.player_img = image
        self.player_img_rect = self.player_img.get_rect()
        walls.append(self)
        self.x = pos[0]
        self.y = pos[1]
        self.hitbox = (self.x,self.y,width,height)
def redrawGameWindow():
    win.blit(background,[0,0])
    ball.draw(win)
    for wall in walls:
        win.blit(walz,(wall.x,wall.y))
        wall.hitbox = (wall.x,wall.y,wall.player_width,wall.player_height)
        pygame.draw.rect(win,(255,0,0),wall.hitbox,2)
    ball.hitbox = (ball.x+5,ball.y+3,ball.player_width-5,ball.player_height-7)
    #pygame.draw.rect(win,(255,0,0),ball.hitbox,2)
    pygame.display.flip()

x = y = 0
for row in map:
    for col in row:
        if col == "W":
            Wall((x, y))
        x += 25
    y += 25
    x = 0
ball = Player(60,60)

run = True
while run:
    clock.tick(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: 
        ball.move(5,0)
    elif keys[pygame.K_RIGHT]:  
        ball.move(-5,0)
    elif keys[pygame.K_UP]:
        ball.move(0,5)
    elif keys[pygame.K_DOWN]:
        ball.move(0,-5)
    win.fill((0,0,0))
    redrawGameWindow()

pygame.quit()