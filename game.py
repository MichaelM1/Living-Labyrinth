import math
import random
import pygame
import items
import maze
import player
from network import Network


pygame.init()

# music
pygame.mixer.init()
WINDOW = pygame.display.set_mode((1296, 720))
pygame.display.set_caption("Living Labyrinth")
CLOCK = pygame.time.Clock()
BACKGROUND = pygame.image.load('assets/background.jpg').convert()
WALZ = pygame.image.load('assets/walls.png')
MENU_SCREEN = pygame.image.load('assets/menuScreen.png').convert()
START_BUTTON = pygame.image.load('assets/start.PNG').convert()
END_SCREEN = pygame.image.load('assets/end.jpg').convert()

MUSIC_LIST = ['Sound/Aria Math.mp3', 'Sound/Beginning 2.mp3', 'Sound/Clark.mp3'
              , 'Sound/Danny.mp3', 'Sound/Dreiton.mp3', 'Sound/Dry Hands.mp3'
              , 'Sound/Haggstrom.mp3', 'Sound/Haunt Muskie.mp3', 'Sound/Living Mice.mp3'
              , 'Sound/Mice On Venus.mp3', 'Sound/Moog City 2.mp3', 'Sound/Mutation.mp3'
              , 'Sound/Subwoofer Lullaby.mp3', 'Sound/Sweden.mp3', 'Sound/Taswell.mp3'
              , 'Sound/Wet Hands.mp3']


class Game(object):
    def __init__(self, width, length, sample_maze, item, data, sample_player, level, sample_player2):
        #self.net = Network()
        self.map_width = width
        self.map_length = length
        self.data = data
        self.maze = sample_maze
        self.run = True
        self.time = 0
        self.item = item
        self.player = sample_player
        self.player2 = sample_player2
        self.level = level
        self.light_radius = 250
        self.torches = []
        self.compass = None
        self.compass_switch = False
        self.fog = pygame.Surface((1296, 720))

    def endStart(self):
        end = True
        while end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    end = False
            WINDOW.fill((0, 0, 0))
            WINDOW.blit(END_SCREEN, [0, 0])
            pygame.display.flip()

    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill((0, 0, 0))
        self.light_rect.center = (self.player.x + 8, self.player.y + 8)
        self.fog.blit(self.light_mask, self.light_rect)
        WINDOW.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)

    def spawn_torches(self):
        side = (self.level + 1) * 4
        lside = (self.level + 1) * 4
        for i in range(self.level + 2):
            if self.level > 1:
                lside = 8
            torch = items.Torch([32 + 64 * random.randint(0, side - 1) + 5, 32 + 64 * random.randint(0, lside - 1)])
            self.torches.append(torch)

    def redrawGameWindow(self):
        WINDOW.blit(BACKGROUND, [0, 0])
        for room in self.data.rooms:
            room.draw(WINDOW)
        self.item.draw(WINDOW)
        for torch in self.torches:
            torch.draw(WINDOW)
        if self.level == 2 and self.compass is not None:
            self.compass.draw(WINDOW)
        self.player.draw(WINDOW)
        self.player2.draw(WINDOW)
        #self.render_fog()
        if self.compass_switch:
            disx = self.item.x - self.player.x
            if disx == 0:
                disx = 1
            disy = self.item.y - self.player.y
            radian = math.atan(disy/disx)
            degree = -(radian * (180/math.pi))
            if disx < 0 and disy > 0:
                degree = -180 + degree
            if disx < 0 and disy < 0:
                degree = 180 + degree
            degree = degree * (math.pi/180)
            x1 = math.cos(degree) * 40
            y1 = math.sin(degree) * -40
            pygame.draw.circle(WINDOW, (105, 105, 105), (1000, 500), 50)
            pygame.draw.circle(WINDOW, (0, 0, 0), (1000, 500), 45)
            pygame.draw.line(WINDOW, (255, 0, 0), (1000, 500), (1000 + x1, 500 + y1), 1)
        pygame.display.flip()

    def update(self, x, y):
        self.player.move(x, y)
        for torch in self.torches:
            if self.player.x > torch.x + 6 or torch.x > self.player.x + 16 or self.player.y > torch.y + 16 or torch.y > self.player.y + 16:
                pass
            else:
                self.torches.remove(torch)
                self.light_radius += 150
        if self.level == 2 and self.compass is not None:
            if (self.player.x > self.compass.x + 16 or self.compass.x > self.player.x + 16) or (self.player.y > self.compass.y + 16 or self.compass.y > self.player.y + 16):
                pass
            else:
                self.compass = None
                self.compass_switch = True
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
        if self.level == 2:
            exit2 = items.Coin([32 + 64 * random.randint(0, side - 1), 32 + 64 * random.randint(0, lside - 1)])
        else:
            exit2 = items.Exit([32 + 64 * random.randint(0, side - 1), 32 + 64 * random.randint(0, lside - 1)])
        maze2 = maze.Maze(data2, lside, side)
        player2 = player.Player(32, 32, data2, maze2, exit2)
        self.__init__(8, 8, maze2, exit2, data2, player2, self.level)
        self.start()
        
    def start(self):
        self.spawn_torches()
        self.maze.MazeSkeleton(0,0)
        self.maze.FillMaze()
        self.maze.ScrambleMaze()
        randomlist = list(range(0, 16))
        random.shuffle(randomlist)
        pygame.mixer_music.load(MUSIC_LIST[randomlist.pop()])
        pygame.mixer_music.set_volume(0.5)
        pygame.mixer_music.play(-1)
        if self.level == 2:
            side = (self.level + 1) * 4
            self.compass = items.Compass([32 + 64 * random.randint(0, side - 1)
                                          , 32 + 64 * random.randint(0, 8 - 1)])
        while self.run:
            self.time += 1
            CLOCK.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.update(3, 0)
                self.player.left = True
                self.player.right = False
                self.player.up = False
                self.player.down = False
            if keys[pygame.K_RIGHT]:
                self.update(-3, 0)
                self.player.left = False
                self.player.right = True
                self.player.up = False
                self.player.down = False
            if keys[pygame.K_UP]:
                self.update(0, 3)
                self.player.left = False
                self.player.right = False
                self.player.up = True
                self.player.down = False
            if keys[pygame.K_DOWN]:
                self.update(0, -3)
                self.player.left = False
                self.player.right = False
                self.player.up = False
                self.player.down = True
            if keys[pygame.K_q]:
                self.run = False
            #self.player.x, self.player.y = self.parse_data(self.send_data())
            if self.time // 5 == 1:
                self.time = 0
                self.light_radius -= 1
                if self.light_radius == 0:
                    self.endStart()
            self.fog.fill((20, 20, 20))
            self.light_mask = pygame.image.load(('assets/light_mask.png')).convert_alpha()
            self.light_mask = pygame.transform.scale(self.light_mask, (self.light_radius, self.light_radius))
            self.light_rect = self.light_mask.get_rect()
            if self.player.end:
                self.increaseLevel()
            WINDOW.fill((0, 0, 0))
            self.redrawGameWindow()

    def send_data(self):
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        print(data)
        reply = self.net.send(data)
        return reply

    def parse_data(self, data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0


def menuStart():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]
            mouse = pygame.mouse.get_pressed()[0]
        WINDOW.fill((0, 0, 0))
        WINDOW.blit(MENU_SCREEN, [0, 0])
        originalImg = pygame.image.load('assets/button.png').convert()
        originalImg_rect = pygame.Rect(0, 0, 365, 94)
        image = pygame.Surface(originalImg_rect.size).convert()
        image.blit(originalImg, (0, 0), originalImg_rect)
        alpha = image.get_at((0, 0))
        image.set_colorkey(alpha)
        WINDOW.blit(image, (450, 200))
        options = pygame.image.load('assets/options.PNG')
        WINDOW.blit(options, (450, 300))
        quit = pygame.image.load('assets/quit.PNG')
        WINDOW.blit(quit, (450, 400))
        if 450 < x < 815 and 200 < y < 294:
            pygame.draw.rect(WINDOW, (255, 0, 0), (450, 200, 365, 94), 2)
        if 450 < x < 815 and 300 < y < 394:
            pygame.draw.rect(WINDOW, (255, 0, 0), (450, 300, 365, 94), 2)
        if 450 < x < 815 and 400 < y < 494:
            pygame.draw.rect(WINDOW, (255, 0, 0), (450, 400, 365, 94), 2)
        if 450 < x < 815 and 200 < y < 294 and mouse == 1:
            game.start()
            menu = False
        if 450 < x < 815 and 300 < y < 394 and mouse == 1:
            print("?")
        if 450 < x < 815 and 400 < y < 494 and mouse == 1:
            menu = False
        pygame.display.flip()

data1 = items.Data()
maze1 = maze.Maze(data1, 4, 4)
exit1 = items.Exit([32 + 64 * random.randint(0, 4 - 1), 32 + 64 * random.randint(0, 4 - 1)])
player1 = player.Player(32, 32, data1, maze1, exit1)
player2 = player.Player(96, 32, data1, maze1, exit1)
game = Game(4, 4, maze1, exit1, data1, player1, 0, player2)
menuStart()
pygame.quit()
