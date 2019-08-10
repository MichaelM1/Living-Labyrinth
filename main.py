import pygame
import random
import wall
import maze
import player

pygame.init()

# music
pygame.mixer.init()
pygame.mixer_music.load("soundtrack.mp3")
pygame.mixer_music.set_volume(0.5)
pygame.mixer_music.play(-1)

win = pygame.display.set_mode((1296, 720))
pygame.display.set_caption("Living Labyrinth")
clock = pygame.time.Clock()
background = pygame.image.load('assets/background.jpg').convert()
walz = pygame.image.load('assets/walls.png')


class Game(object):

    def __init__(self):
        self.map_width = 45
        self.map_length = 81
        self.grid_width = self.map_width // 4
        self.grid_length = self.map_length // 4
        self.data = wall.Data()
        self.maze = maze.Maze(self.data, self.map_width, self.map_length, self.grid_width, self.grid_length)
        self.player = player.Player(352, 352, self.data, self.maze)
        self.run = True
        self.time = 0

    def redrawGameWindow(self):
        win.blit(background, [0, 0])
        for wall in self.data.walls:
            wall.draw(win)
        self.player.draw(win)
        pygame.display.flip()

    def update(self, x, y):
        self.player.move(x, y)
        self.player.checkForCollision(x, y)
        self.player.checkForSteps(x, y)

    def start(self):
        self.maze.mazeSkeleton()
        self.maze.fillMaze(0, 0)
        self.maze.scrambleMaze(32, 32)
        while self.run:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.update(3, 0)
            if keys[pygame.K_RIGHT]:
                self.update(-3, 0)
            if keys[pygame.K_UP]:
                self.update(0, 3)
            if keys[pygame.K_DOWN]:
                self.update(0, -3)
            win.fill((0, 0, 0))
            self.redrawGameWindow()


game = Game()
game.start()

pygame.quit()
