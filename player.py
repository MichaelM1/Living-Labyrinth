import maze
import wall
import pygame
import time

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16
HITBOX_LEEWAY = 3
WALL_SIZE = 16


class Player(object):
    def __init__(self, x, y, data, maze):
        self.x = x
        self.y = y
        self.width = width = PLAYER_WIDTH
        self.height = height = PLAYER_HEIGHT
        self.triggerX = 0
        self.triggerY = 0
        spritesheet = pygame.image.load('assets/player.png').convert()
        sprite_rect = pygame.Rect(0, 0, width, height)
        image = pygame.Surface(sprite_rect.size).convert()
        image.blit(spritesheet, (0, 0), sprite_rect)
        alpha = image.get_at((0, 0))
        image.set_colorkey(alpha)
        self.player_img = image
        self.player_img_rect = self.player_img.get_rect()
        self.data = data
        self.maze = maze
        self.collision = False
        self.stepsX = 0
        self.stepsY = 0

    def draw(self, win):
        win.blit(self.player_img, (self.x, self.y))
        self.hitbox = (self.x, self.y, 16, 16)

    def move(self, dx, dy):
        # for s in range(len(self.data.wallsStr)):
        # l = self.data.wallsStr[s].split(',')
        # i1 = l[1].index(')')
        # i = l[0].index('(')
        # l1 = (l[0])[i + 1:]
        # l2 = (l[1])[0:i1]
        # s1 = 'Wall(' + str(int(l1) + dx) +',' + str(int(l2) + dy) + ")"
        # self.data.wallsStr[s] = s1
        # for wall in self.data.walls:
        self.x -= dx
        self.y -= dy

    def checkForCollision(self, dx, dy):
        for wall in self.data.walls:
            if self.x > (wall.x + HITBOX_LEEWAY + WALL_SIZE - (HITBOX_LEEWAY * 2)) or wall.x + HITBOX_LEEWAY > (
                    self.x + 16):
                self.collision = False
            elif self.y > (wall.y + HITBOX_LEEWAY + WALL_SIZE - (HITBOX_LEEWAY * 2)) or wall.y + HITBOX_LEEWAY > (
                    self.y + 16):
                self.collision = False
            else:
                self.collision = True
                break
        if self.collision:
            # for wall in self.data.walls:
            self.x += dx
            self.y += dy

    def checkForSteps(self, dx, dy):
        if self.collision == False:
            self.triggerX += dx
            self.triggerY += dy
            self.stepsX += dx
            self.stepsY += dy
            if (abs(self.triggerX) + abs(self.triggerY) > (12 * 16)):
                self.triggerX = 0
                self.triggerY = 0
                # self.maze.fillMaze(self.stepsX, self.stepsY)
                self.maze.fillMaze(0, 0)
                # i = 32 + self.stepsX
                # j = 32 + self.stepsY
                # self.maze.scrambleMaze(i, j)
                self.maze.scrambleMaze(32, 32)
