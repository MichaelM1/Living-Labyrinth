import pygame

HITBOX_LEEWAY = 3
WALL_SIZE = 16
EXIT_SIZE = 16

class Room(object):
    def __init__(self, pos, x, y):
        self.row = pos[0]
        self.col = pos[1]
        self.x = x
        self.y = y
        self.right = True
        self.left = True
        self.up = True
        self.down = True
        self.wallImg = pygame.image.load('assets/walls.png')

    def __str__(self):
        return "Room("+ str(self.row)+","+ str(self.col)+")"

    def draw(self, win):
        win.blit(self.wallImg, (self.x, self.y))
        win.blit(self.wallImg, (self.x + 16, self.y))
        if self.up:
            win.blit(self.wallImg, (self.x + 32, self.y))
        win.blit(self.wallImg, (self.x + 48, self.y))
        win.blit(self.wallImg, (self.x + 64, self.y))
        win.blit(self.wallImg, (self.x + 64, self.y + 16))
        if self.right:
            win.blit(self.wallImg, (self.x + 64, self.y +32))
        win.blit(self.wallImg, (self.x + 64, self.y + 48))
        win.blit(self.wallImg, (self.x + 64, self.y + 64))
        win.blit(self.wallImg, (self.x + 48, self.y + 64))
        if self.down:
            win.blit(self.wallImg, (self.x + 32, self.y + 64))
        win.blit(self.wallImg, (self.x +16, self.y + 64))
        win.blit(self.wallImg, (self.x, self.y + 64))
        win.blit(self.wallImg, (self.x, self.y + 48))
        if self.left:
            win.blit(self.wallImg, (self.x, self.y + 32))
        win.blit(self.wallImg, (self.x, self.y + 16))

class Exit(object):
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.originalImg = pygame.image.load('assets/ladder.png').convert()
        originalImg_rect = pygame.Rect(0, 0, 16, 16)
        image = pygame.Surface(originalImg_rect.size).convert()
        image.blit(self.originalImg, (0, 0), originalImg_rect)
        alpha = image.get_at((0, 0))
        image.set_colorkey(alpha)
        self.exitImg = image
        self.hitbox = (self.x, self.y, EXIT_SIZE, EXIT_SIZE)
        self.endImg = pygame.image.load('assets/coin1.png').convert()
    
    def draw(self, win):
        win.blit(self.exitImg, (self.x, self.y))
    
    def drawEnd(self,win):
        win.blit(self.endImg, (self.x, self.y))
    
class Data(object):
    def __init__(self):
        self.rooms = []
        self.roomsStr = []

    def Add(self, object):
        self.rooms.append(object)
    
    def AddString(self, string):
        self.roomsStr.append(string)