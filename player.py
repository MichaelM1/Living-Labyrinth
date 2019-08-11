import pygame

#PLAYER_WIDTH = 2560
#PLAYER_HEIGHT = 1440
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16
HITBOX_LEEWAY = 3
WALL_SIZE = 16
walkRight = [pygame.image.load('assets/right0.png'), pygame.image.load('assets/right1.png'), pygame.image.load('assets/right2.png')]
walkLeft = [pygame.image.load('assets/left0.png'), pygame.image.load('assets/left1.png'), pygame.image.load('assets/left2.png')]
walkUp = [pygame.image.load('assets/up0.png'), pygame.image.load('assets/up1.png'), pygame.image.load('assets/up2.png')]
walkDown = [pygame.image.load('assets/down0.png'), pygame.image.load('assets/down1.png'), pygame.image.load('assets/down2.png')]

class Player(object):
    def __init__(self, x, y, data, maze, exit):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.x = x
        self.y = y
        self.width = width = PLAYER_WIDTH
        self.height = height = PLAYER_HEIGHT
        self.triggerX = 0
        self.triggerY = 0
        self.player_img = pygame.image.load('assets/player.png').convert()
        self.player_img_rect = self.player_img.get_rect()
        self.data = data
        self.maze = maze
        self.collision = False
        self.stepsX = 0
        self.stepsY = 0
        self.exit = exit
        self.end = False
        self.walk_count = 0
        self.walk_right = [pygame.image.load('assets/right01.png'), pygame.image.load('assets/right11.png'), pygame.image.load('assets/right21.png')]
        self.walk_left = [pygame.image.load('assets/left01.png'), pygame.image.load('assets/left11.png'), pygame.image.load('assets/left21.png')]
        self.walk_up = [pygame.image.load('assets/up01.png'), pygame.image.load('assets/up11.png'), pygame.image.load('assets/up21.png')]
        self.walk_down = [pygame.image.load('assets/down01.png'), pygame.image.load('assets/down11.png'), pygame.image.load('assets/down21.png')]

    def draw(self, win):
        #win.blit(self.player_img, (self.x - 1319, self.y - 708))
        if self.walk_count > 20:
            self.walk_count = 0
        spritesheet = pygame.image.load('assets/up01.png')
        if self.left:
            spritesheet = self.walk_left[self.walk_count//10]
        if self.right:
            spritesheet = self.walk_right[self.walk_count//10]
        if self.up:
            spritesheet = self.walk_up[self.walk_count//10]
        if self.down:
            spritesheet = self.walk_down[self.walk_count//10]
        sprite_rect = pygame.Rect(0, 0, self.width, self.height)
        image = pygame.Surface(sprite_rect.size).convert()
        image.blit(spritesheet, (0, 0), sprite_rect)
        alpha = image.get_at((0, 0))
        image.set_colorkey(alpha)
        self.player_img = image
        win.blit(self.player_img, (self.x, self.y))
        self.hitbox = (self.x, self.y, 16, 16)

    def move(self, dx, dy):
        self.walk_count +=1
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
            self.x += dx
            self.y += dy
        if self.x > (self.exit.x + HITBOX_LEEWAY + WALL_SIZE - (HITBOX_LEEWAY * 2)) or self.exit.x + HITBOX_LEEWAY > (
            self.x + 16):
            self.end = False
        elif self.y > (self.exit.y + HITBOX_LEEWAY + WALL_SIZE - (HITBOX_LEEWAY * 2)) or self.exit.y + HITBOX_LEEWAY > (
            self.y + 16):
            self.end = False
        else:
            self.end = True

    def checkForSteps(self, dx, dy):
        if not self.collision:
            self.triggerX += dx
            self.triggerY += dy
        if abs(self.triggerX) + abs(self.triggerY) > (8 * 16):
            self.triggerX = 0
            self.triggerY = 0
            self.maze.fillMaze(0, 0)
            self.maze.scrambleMaze(32, 32)
