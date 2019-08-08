import pygame
import random

# declare constants
WALL_SIZE = 16
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16
HITBOX_LEEWAY = 3

pygame.init()

# setup display window for pygame with background
window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Living Labyrinth")
clock = pygame.time.Clock()
background = pygame.image.load('assets/background.jpg').convert()
wallIMG = pygame.image.load('assets/walls.png').convert()

# declare additional variables for helper functions
walls = []
wallsStr = []
s = 32
x = y = 0
w = 64
grid = []
visited = []
stack = []

# set up layout of map. W's correspond to walls and S's correspond to changing walls
map = [
    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W",
     "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
    ["W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ",
     " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W"],
    ["W", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ",
     " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "W"],
    ["W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ",
     " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W"],
    ["W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S",
     "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W"],
    ["W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ",
     " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W"],
    ["W", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ",
     " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "W"],
    ["W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ",
     " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W"],
    ["W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S",
     "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W"],
    ["W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ",
     " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W"],
    ["W", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ",
     " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "W"],
    ["W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ",
     " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W"],
    ["W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S",
     "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W"],
    ["W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ",
     " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W"],
    ["W", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ",
     " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "W"],
    ["W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ",
     " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W"],
    ["W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S",
     "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W"],
    ["W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ",
     " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W"],
    ["W", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ",
     " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "W"],
    ["W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ",
     " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W"],
    ["W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S",
     "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W"],
    ["W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ",
     " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W"],
    ["W", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ",
     " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "W"],
    ["W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ",
     " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W"],
    ["W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S",
     "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W", "W", "S", "W", "W"],
    ["W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ",
     " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W"],
    ["W", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ",
     " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "S", " ", " ", " ", "W"],
    ["W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ",
     " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W", " ", " ", " ", "W"],
    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W",
     "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"], ]


# Initiated with a position in the window
class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH	
        self.height = PLAYER_HEIGHT
        self.triggerX = 0
        self.triggerY = 0
        spritesheet = pygame.image.load('assets/player.png').convert()
        sprite_rect = pygame.Rect(0, 0, self.width, self.height)
        image = pygame.Surface(sprite_rect.size).convert()
        image.blit(spritesheet, (0, 0), sprite_rect)
        alpha = image.get_at((0, 0))
        image.set_colorkey(alpha)
        self.player_img = image
        self.player_img_rect = self.player_img.get_rect()

    def draw(self, window):
        window.blit(self.player_img, (self.x, self.y))

    def move(self, dx, dy):
        self.x -= dx
        self.y -= dy
        collision = False
        for wall in walls:
            # if wall and player rectangle overlap, revert movement
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
        # if player moves, check if player has exceeded movement for changing walls
        if collision == False:
            self.triggerX += dx
            self.triggerY += dy
            if abs(self.triggerX) + abs(self.triggerY) > (12 * 16):
                self.triggerX = 0
                self.triggerY = 0
                fillMaze()
                scrambleMaze()


# Initiated with a position in the window
class Wall(object):
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        walls.append(self)
        wallsStr.append(str(self))
        self.hitbox = (self.x + HITBOX_LEEWAY, self.y + HITBOX_LEEWAY, WALL_SIZE - (HITBOX_LEEWAY * 2), WALL_SIZE - (HITBOX_LEEWAY * 2))

    def __str__(self):
        return "Wall(" + str(self.x) + "," + str(self.y) + ")"

    def draw(self, window):
        window.blit(wallIMG, (self.x, self.y))


def redrawGameWindow():
    window.blit(background, [0, 0])
    player.draw(window)
    # Draw all walls that exist inside list walls
    for wall in walls:
        wall.draw(window)
        # pygame.draw.rect(window, (0, 0, 255), wall.hitbox, 2) #draw wall hitbox
    # pygame.draw.rect(window,(255,0,0),(player.x, player.y, player.width, player.height),2)
    pygame.display.flip()


def up(x, y):
    y = y - s
    i = wallsStr.index('Wall(' + str(x) + ',' + str(y) + ')')
    del walls[i]
    del wallsStr[i]


def down(x, y):
    y = y + s
    i = wallsStr.index('Wall(' + str(x) + ',' + str(y) + ')')
    del walls[i]
    del wallsStr[i]


def left(x, y):
    x = x - s
    i = wallsStr.index('Wall(' + str(x) + ',' + str(y) + ')')
    del walls[i]
    del wallsStr[i]


def right(x, y):
    x = x + s
    i = wallsStr.index('Wall(' + str(x) + ',' + str(y) + ')')
    del walls[i]
    del wallsStr[i]


# create changing walls in window as wall objects corresponding to all "S" variables
def fillMaze():
    for row in range(len(map)):
        for col in range(len(map[0])):
            if map[row][col] == "S":
                x = col * WALL_SIZE
                y = row * WALL_SIZE
                i = 'Wall(' + str(x) + ',' + str(y) + ')'
                if i not in wallsStr:
                    Wall((x, y))


def scrambleMaze(x=32, y=32):
    # append first room position to stack and visited list
    stack.append((x, y))
    visited.append((x, y))
    while len(stack) > 0:
        cell = []
        # find non-visited locations that are in the grid
        if (x + w, y) not in visited and (x + w, y) in grid:
            cell.append("right")
        if (x - w, y) not in visited and (x - w, y) in grid:
            cell.append("left")
        if (x, y + w) not in visited and (x, y + w) in grid:
            cell.append("down")
        if (x, y - w) not in visited and (x, y - w) in grid:
            cell.append("up")
        if len(cell) > 0:
            cell_chosen = (random.choice(cell))
            # if there is a non-visited location, access it and add it to the lists
            if cell_chosen == "right":
                right(x, y)
                x = x + w
                visited.append((x, y))
                stack.append((x, y))
            elif cell_chosen == "left":
                left(x, y)
                x = x - w
                visited.append((x, y))
                stack.append((x, y))
            elif cell_chosen == "down":
                down(x, y)
                y = y + w
                visited.append((x, y))
                stack.append((x, y))
            elif cell_chosen == "up":
                up(x, y)
                y = y - w
                visited.append((x, y))
                stack.append((x, y))
        # if not remove variables from stack until non-visited locations are available
        else:
            x, y = stack.pop()
    stack.clear()
    visited.clear()


# fill in positions for all rooms in window
def build_grid(x, y):
    for i in range(1, 8):
        x = 32
        y = y + 64
        for j in range(1, 11):
            grid.append((x, y))
            x = x + 64


# create non-changing walls in window as wall objects corresponding to all "W" variables
for row in range(len(map)):
    for col in range(len(map[0])):
        if map[row][col] == "W":
            Wall((col * WALL_SIZE, row * WALL_SIZE))

build_grid(32, -32)

player = Player(32, 32)
fillMaze()
scrambleMaze()
run = True
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(2, 0)
    elif keys[pygame.K_RIGHT]:
        player.move(-2, 0)
    elif keys[pygame.K_UP]:
        player.move(0, 2)
    elif keys[pygame.K_DOWN]:
        player.move(0, -2)
    window.fill((0, 0, 0))
    redrawGameWindow()

pygame.quit()
