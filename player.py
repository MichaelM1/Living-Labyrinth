import maze
import wall
import pygame
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16
class Player(object):
    def __init__(self, x, y,data, maze): 
        self.x = x
        self.y = y
        self.width = width = PLAYER_WIDTH
        self.height = height = PLAYER_HEIGHT
        self.triggerX= 0
        self.triggerY=0
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

    def draw(self, win):
        win.blit(self.player_img, (self.x, self.y))

    def move(self, dx, dy):
        self.x -= dx
        self.y -= dy
        collision = False
        for wall in self.data.walls:
            if self.x > (wall.hitbox[0] + wall.hitbox[2]) or wall.hitbox[0] > (self.x + self.width):
                collision = False
            elif self.y > (wall.hitbox[1] + wall.hitbox[3]) or wall.hitbox[1] > (self.y + self.height):
                collision = False
            else: 
                collision = True
                break
        if collision:
            self.x += dx
            self.y += dy
        if collision == False:
            self.triggerX +=dx
            self.triggerY +=dy
            if(abs(self.triggerX) + abs(self.triggerY)>(12*16)):
                self.triggerX = 0
                self.triggerY = 0
                self.maze.fillMaze()                  
                self.maze.scrambleMaze()