import pygame
import items
import maze
import player
import random

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
endScreen = pygame.image.load('assets/end.jpg').convert()

musiclist = ['Sound/Aria Math.mp3', 'Sound/Beginning 2.mp3', 'Sound/Clark.mp3', 'Sound/Danny.mp3',
             'Sound/Dreiton.mp3', 'Sound/Dry Hands.mp3', 'Sound/Haggstrom.mp3', 'Sound/Haunt Muskie.mp3',
             'Sound/Living Mice.mp3', 'Sound/Mice On Venus.mp3', 'Sound/Moog City 2.mp3',
             'Sound/Mutation.mp3', 'Sound/Subwoofer Lullaby.mp3', 'Sound/Sweden.mp3', 'Sound/Taswell.mp3',
             'Sound/Wet Hands.mp3']


class Game(object):
    def __init__(self, width, length, maze, exit, data, player, level):
        self.map_width = width
        self.map_length = length
        self.data = data
        self.maze = maze
        self.run = True
        self.time = 0
        self.exit = exit
        self.player = player
        self.level = level

    def endStart(self):
        end = True
        while end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    end = False
            win.fill((0, 0, 0))
            win.blit(endScreen, [0, 0])
            pygame.display.flip()

    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill((0, 0, 0))
        self.light_rect.center = (self.player.x + 8, self.player.y + 8)
        self.fog.blit(self.light_mask, self.light_rect)
        win.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)

    def redrawGameWindow(self):
        win.blit(background, [0, 0])
        for room in self.data.rooms:    
            room.draw(win)
        if self.level == 2:
            self.exit.drawEnd(win)
        else:
            self.exit.draw(win)
        self.player.draw(win)
        self.render_fog()
        pygame.display.flip()

    def update(self, x, y):
        self.player.move(x, y)
        self.player.CheckForCollision(x, y)
        self.player.checkForSteps(x, y)

    def increaseLevel(self):
        self.level += 1
        if self.level == 3:
            self.endStart()
        side = (self.level + 1) * 4
        lside = (self.level + 1) * 4
        data2 = items.Data()
        if self.level > 1:
            lside = 8
        maze2 = maze.Maze(data2, lside, side)
        exit2 = items.Exit([32 + 64 * random.randint(0, side - 1), 32 + 64 * random.randint(0, lside - 1)])
        player2 = player.Player(32, 32, data2, maze2, exit2)
        self.__init__(8,8, maze2, exit2, data2, player2, self.level)
        self.start()

    def start(self):
        self.maze.MazeSkeleton(0,0)
        self.maze.FillMaze()
        self.maze.ScrambleMaze()
        randomlist = list(range(0, 16))
        random.shuffle(randomlist)
        pygame.mixer_music.load(musiclist[randomlist.pop()])
        pygame.mixer_music.set_volume(0.5)
        pygame.mixer_music.play(-1)
        while self.run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.update(3,0)
                self.player.left = True
                self.player.right = False
                self.player.up = False
                self.player.down = False
            if keys[pygame.K_RIGHT]:
                self.update(-3,0)
                self.player.left = False
                self.player.right = True
                self.player.up = False
                self.player.down = False
            if keys[pygame.K_UP]:
                self.update(0,3)
                self.player.left = False
                self.player.right = False
                self.player.up = True
                self.player.down = False
            if keys[pygame.K_DOWN]:
                self.update(0,-3)
                self.player.left = False
                self.player.right = False
                self.player.up = False
                self.player.down = True
            if keys[pygame.K_q]:
                self.run = False
            win.fill((0, 0, 0))
            self.fog = pygame.Surface((1296, 720))
            self.fog.fill((20, 20, 20))
            self.light_mask = pygame.image.load(('assets/light_mask.png')).convert_alpha()
            self.light_mask = pygame.transform.scale(self.light_mask, (250, 250))
            self.light_rect = self.light_mask.get_rect()
            if self.player.end:
                self.increaseLevel()
            self.redrawGameWindow()

data1 = items.Data()
maze1 = maze.Maze(data1, 4, 4)
exit1 = items.Exit([32 + 64 * random.randint(0, 4 - 1), 32 + 64 * random.randint(0, 4 - 1)])
player1 = player.Player(32, 32, data1, maze1, exit1)
game = Game(4, 4, maze1, exit1, data1, player1, 0)


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
