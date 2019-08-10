import pygame, sys, random, time
import wall
import maze
import player

pygame.init()

#music
pygame.mixer.init()
pygame.mixer_music.load("soundtrack.mp3")
pygame.mixer_music.set_volume(0.5)
pygame.mixer_music.play(-1)

win = pygame.display.set_mode((1296, 720))
pygame.display.set_caption("Living Labyrinth")
clock = pygame.time.Clock()
background = pygame.image.load('assets/background.jpg').convert()
walz = pygame.image.load('assets/walls.png')

map_width = 45
map_length = 87
data = wall.Data()
maze = maze.Maze(data)
x = y = 0
run = True
player = player.Player(32, 32, data, maze)



def redrawGameWindow():
    win.blit(background, [0, 0])
    for wall in data.walls:
        wall.draw(win)
    player.draw(win)
    pygame.display.flip()

def startMaze():
    x = y = 0
    for row in range(45):
        for col in range(87):
            if row == 0 or row == 44:
                data.add(wall.Wall((x, y)))
                data.addString(str(wall.Wall((x, y))))
            elif row % 4 == 0 and (col - 2) % 4 != 0:
                data.add(wall.Wall((x, y)))
                data.addString(str(wall.Wall((x, y))))
            elif row % 2 == 1 and col % 4 == 0:
                data.add(wall.Wall((x, y)))
                data.addString(str(wall.Wall((x, y))))
            elif (row - 2) % 4 == 0 and col == 0 or col == 86:
                data.add(wall.Wall((x, y)))
                data.addString(str(wall.Wall((x, y))))
            x += 16
        y += 16
        x = 0


startMaze()
maze.fillMaze()
maze.scrambleMaze()

while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(2, 0)
    if keys[pygame.K_RIGHT]:
        player.move(-2, 0)
    if keys[pygame.K_UP]:
        player.move(0, 2)
    if keys[pygame.K_DOWN]:
        player.move(0, -2)
    win.fill((0, 0, 0))
    redrawGameWindow()

pygame.quit()
