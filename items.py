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
        return "Room(" + str(self.row) + "," + str(self.col) + ")"

    def draw(self, WINDOW):
        WINDOW.blit(self.wallImg, (self.x, self.y))
        WINDOW.blit(self.wallImg, (self.x + 16, self.y))
        if self.up:
            WINDOW.blit(self.wallImg, (self.x + 32, self.y))
        WINDOW.blit(self.wallImg, (self.x + 48, self.y))
        WINDOW.blit(self.wallImg, (self.x + 64, self.y))
        WINDOW.blit(self.wallImg, (self.x + 64, self.y + 16))
        if self.right:
            WINDOW.blit(self.wallImg, (self.x + 64, self.y + 32))
        WINDOW.blit(self.wallImg, (self.x + 64, self.y + 48))
        WINDOW.blit(self.wallImg, (self.x + 64, self.y + 64))
        WINDOW.blit(self.wallImg, (self.x + 48, self.y + 64))
        if self.down:
            WINDOW.blit(self.wallImg, (self.x + 32, self.y + 64))
        WINDOW.blit(self.wallImg, (self.x + 16, self.y + 64))
        WINDOW.blit(self.wallImg, (self.x, self.y + 64))
        WINDOW.blit(self.wallImg, (self.x, self.y + 48))
        if self.left:
            WINDOW.blit(self.wallImg, (self.x, self.y + 32))
        WINDOW.blit(self.wallImg, (self.x, self.y + 16))


class Item(object):
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.hitbox = (self.x, self.y, EXIT_SIZE, EXIT_SIZE)

    def draw(self, WINDOW):
        pass


class Torch(Item):
    def draw(self, WINDOW):
        originalImg = pygame.image.load('assets/torch.png').convert()
        originalImg_rect = pygame.Rect(0, 0, 6, 16)
        image = pygame.Surface(originalImg_rect.size).convert()
        image.blit(originalImg, (0, 0), originalImg_rect)
        alpha = image.get_at((0, 0))
        image.set_colorkey(alpha)
        exitImg = image
        WINDOW.blit(exitImg, (self.x, self.y))

class Boots(Item):
    def draw(self, WINDOW):
        originalImg = pygame.image.load('assets/boots.png').convert()
        originalImg_rect = pygame.Rect(3, 0, 12, 16)
        image = pygame.Surface(originalImg_rect.size).convert()
        image.blit(originalImg, (0, 0), originalImg_rect)
        alpha = image.get_at((0, 0))
        image.set_colorkey(alpha)
        exitImg = image
        WINDOW.blit(exitImg, (self.x, self.y))

class Compass(Item):
    def draw(self, WINDOW):
        originalImg = pygame.image.load('assets/compass.png').convert()
        originalImg_rect = pygame.Rect(0, 0, 16, 16)
        image = pygame.Surface(originalImg_rect.size).convert()
        image.blit(originalImg, (0, 0), originalImg_rect)
        alpha = image.get_at((0, 0))
        image.set_colorkey(alpha)
        exitImg = image
        WINDOW.blit(exitImg, (self.x, self.y))


class Exit(Item):
    def draw(self, WINDOW):
        originalImg = pygame.image.load('assets/ladder.png').convert()
        originalImg_rect = pygame.Rect(0, 0, 16, 16)
        image = pygame.Surface(originalImg_rect.size).convert()
        image.blit(originalImg, (0, 0), originalImg_rect)
        alpha = image.get_at((0, 0))
        image.set_colorkey(alpha)
        exitImg = image
        WINDOW.blit(exitImg, (self.x, self.y))


class Coin(Item):
    def draw(self, WINDOW):
        originalImg = pygame.image.load('assets/coin1.png').convert()
        originalImg_rect = pygame.Rect(0, 0, 16, 16)
        image = pygame.Surface(originalImg_rect.size).convert()
        image.blit(originalImg, (0, 0), originalImg_rect)
        alpha = image.get_at((0, 0))
        image.set_colorkey(alpha)
        exitImg = image
        WINDOW.blit(exitImg, (self.x, self.y))


class Data(object):
    def __init__(self):
        self.rooms = []
        self.roomsStr = []

    def Add(self, room_id):
        self.rooms.append(room_id)

    def AddString(self, string):
        self.roomsStr.append(string)
