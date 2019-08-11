import pygame
import random
import wall
import maze
import player

pygame.init()

# music
pygame.mixer.init()
win = pygame.display.set_mode((1296, 720))
pygame.display.set_caption("Living Labyrinth")
clock = pygame.time.Clock()
background = pygame.image.load('assets/background.jpg').convert()
walz = pygame.image.load('assets/walls.png')
menuScreen = pygame.image.load('assets/menuScreen.png').convert()
startButton = pygame.image.load('assets/start.PNG').convert()

musiclist = ['Sound/Aria Math.mp3', 'Sound/Beginning 2.mp3', 'Sound/Clark.mp3', 'Sound/Danny.mp3',
             'Sound/Dreiton.mp3', 'Sound/Dry Hands.mp3', 'Sound/Haggstrom.mp3', 'Sound/Haunt Muskie.mp3',
             'Sound/Living Mice.mp3', 'Sound/Mice On Venus.mp3', 'Sound/Minecraft.mp3', 'Sound/Moog City 2.mp3',
             'Sound/Mutation.mp3', 'Sound/Subwoofer Lullaby.mp3', 'Sound/Sweden.mp3', 'Sound/Taswell.mp3',
             'Sound/Wet Hands.mp3']


class Game(object):

    def __init__(self):
        self.map_width = 45
        self.map_length = 81
        self.grid_width = self.map_width // 4
        self.grid_length = self.map_length // 4
        self.data = wall.Data()
        self.maze = maze.Maze(self.data, self.map_width, self.map_length, self.grid_width, self.grid_length)
        self.run = True
        self.time = 0
        self.player = player.Player(352, 352, self.data, self.maze)

    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill((0, 0, 0))
        self.light_rect.center = (self.player.x + 8, self.player.y + 8)
        self.fog.blit(self.light_mask, self.light_rect)
        win.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)

    def redrawGameWindow(self):
        win.blit(background, [0, 0])
        for wall in self.data.walls:
            wall.draw(win)
        self.player.draw(win)
        self.render_fog()
        pygame.display.flip()

    def update(self, x, y):
        self.player.move(x, y)
        self.player.checkForCollision(x, y)
        self.player.checkForSteps(x, y)

    def start(self):
        self.maze.mazeSkeleton()
        self.maze.fillMaze(0, 0)
        self.maze.scrambleMaze(32, 32)
        randomlist = list(range(0, 16))
        random.shuffle(randomlist)
        pygame.mixer_music.load(musiclist[randomlist.pop()])
        pygame.mixer_music.set_volume(0.5)
        pygame.mixer_music.play(-1)
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
            self.fog = pygame.Surface((1296, 720))
            self.fog.fill((20, 20, 20))
            self.light_mask = pygame.image.load(('assets/light_mask.png')).convert_alpha()
            self.light_mask = pygame.transform.scale(self.light_mask, (250, 250))
            self.light_rect = self.light_mask.get_rect()
            self.redrawGameWindow()


game = Game()


def menuStart():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]
            mouse = pygame.mouse.get_pressed()[0]
        win.fill((0, 0, 0))
        win.blit(menuScreen, [0, 0])
        originalImg = pygame.image.load('assets/button.png').convert()
        originalImg_rect = pygame.Rect(0, 0, 365, 94)
        image = pygame.Surface(originalImg_rect.size).convert()
        image.blit(originalImg, (0, 0), originalImg_rect)
        alpha = image.get_at((0, 0))
        image.set_colorkey(alpha)
        win.blit(image, (450, 200))
        options = pygame.image.load('assets/options.PNG')
        win.blit(options, (450, 300))
        quit = pygame.image.load('assets/quit.PNG')
        win.blit(quit, (450, 400))
        if 450 < x < 815 and 200 < y < 294:
            pygame.draw.rect(win, (255, 0, 0), (450, 200, 365, 94), 2)
        if 450 < x < 815 and 300 < y < 394:
            pygame.draw.rect(win, (255, 0, 0), (450, 300, 365, 94), 2)
        if 450 < x < 815 and 400 < y < 494:
            pygame.draw.rect(win, (255, 0, 0), (450, 400, 365, 94), 2)
        if 450 < x < 815 and 200 < y < 294 and mouse == 1:
            game.start()
            menu = False
        if 450 < x < 815 and 300 < y < 394 and mouse == 1:
            print("?")
        if 450 < x < 815 and 400 < y < 494 and mouse == 1:
            menu = False
        pygame.display.flip()


menuStart()

pygame.quit()
