import pygame

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16
HITBOX_LEEWAY = 3
WALL_SIZE = 16

class Player(object):
    def __init__(self, x, y, data, maze, exit):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.exit = exit
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.triggerX = 0
        self.triggerY = 0
        self.player_img = pygame.image.load('assets/player.png').convert()
        self.player_img_rect = self.player_img.get_rect()
        self.data = data
        self.maze = maze
        self.collision = False
        self.stepsX = 0
        self.stepsY = 0
        self.end = False
        self.walk_count = 0
        self.walk_right = [pygame.image.load('assets/right01.png'), pygame.image.load('assets/right11.png'), pygame.image.load('assets/right21.png')]
        self.walk_left = [pygame.image.load('assets/left01.png'), pygame.image.load('assets/left11.png'), pygame.image.load('assets/left21.png')]
        self.walk_up = [pygame.image.load('assets/up01.png'), pygame.image.load('assets/up11.png'), pygame.image.load('assets/up21.png')]
        self.walk_down = [pygame.image.load('assets/down01.png'), pygame.image.load('assets/down11.png'), pygame.image.load('assets/down21.png')]

    def draw(self, win):
        #win.blit(self.player_img, (self.x - 1319, self.y - 708))
        if self.walk_count > 14:
            self.walk_count = 0
        spritesheet = pygame.image.load('assets/up01.png')
        if self.left:
            spritesheet = self.walk_left[self.walk_count//5]
        if self.right:
            spritesheet = self.walk_right[self.walk_count//5]
        if self.up:
            spritesheet = self.walk_up[self.walk_count//5]
        if self.down:
            spritesheet = self.walk_down[self.walk_count//5]
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
        if (self.x > self.exit.x + 16 or self.exit.x > self.x + 16) or (self.y > self.exit.y + 16 or self.exit.y > self.y + 16):
            self.end = False
        else:
            self.end = True

    def CheckForCollision(self, dx, dy):
        col = (self.x - 14) // 64
        row = (self.y - 14) // 64

        i = self.data.roomsStr.index('Room(' + str(row) + ',' + str(col) + ')')
        if self.x > 16 + 64 * col and self.x < 48 + 64 * col and self.y > 16 + 64 * row and self.y < 48 + 64 * row:
            self.collision = False
        elif not self.data.rooms[i].right and self.x > 45 + 64 * col and self.y > 30 + 64 * row and self.y < 35 + 64 * row:
            self.collision = False
        elif not self.data.rooms[i].down and self.x > 30 + 64 * col and self.x < 35 + 64 * col and self.y > 45 + 64 * row:
            self.collision = False
        elif not self.data.rooms[i].left and self.x < 19 + 64 * col and self.y > 30 + 64 * row and self.y < 35 + 64 * row:
            self.collision = False
        elif not self.data.rooms[i].up and self.x > 30 + 64 * col and self.x < 35 + 64 * col and self.y < 19 + 64 * row:
            self.collision = False
        else:
            self.collision = True
        if self.collision:
            self.x += dx
            self.y += dy

    def checkForSteps(self, dx, dy):
        if not self.collision:
            self.triggerX += dx
            self.triggerY += dy
        if not self.collision and abs(self.triggerX) + abs(self.triggerY) > (16 * 16):
            self.triggerX = 0
            self.triggerY = 0
            col = (self.x - 16) // 64
            row = (self.y - 16) // 64
            if self.x > 16 + 64 * col and self.x < 48 + 64 * col and self.y > 16 + 64 * row and self.y < 48 + 64 * row:    
                self.maze.FillMaze()
                self.maze.ScrambleMaze()
                print("hi")