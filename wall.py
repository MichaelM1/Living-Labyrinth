import pygame

HITBOX_LEEWAY = 3
WALL_SIZE = 16


class Wall(object):

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.wallImg = pygame.image.load('assets/walls.png')
        self.hitbox = (self.x + HITBOX_LEEWAY, self.y + HITBOX_LEEWAY, WALL_SIZE - (HITBOX_LEEWAY * 2),
                       WALL_SIZE - (HITBOX_LEEWAY * 2))

    def __str__(self):
        return "Wall(" + str(self.x) + "," + str(self.y) + ")"

    def draw(self, win):
        win.blit(self.wallImg, (self.x, self.y))


class Data(object):

    def __init__(self):
        self.walls = []
        self.wallsStr = []

    def add(self, object):
        self.walls.append(object)

    def addString(self, string):
        self.wallsStr.append(string)
