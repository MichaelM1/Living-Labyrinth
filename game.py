import math
import random
import pygame
import items
import maze
import player
from network import Network


pygame.init()
pygame.font.init()
pygame.mixer.init()
WINDOW = pygame.display.set_mode((1296, 720))
pygame.display.set_caption("Living Labyrinth")
CLOCK = pygame.time.Clock()
BACKGROUND = pygame.image.load('assets/background.jpg').convert()
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
    def __init__(self, width, length, level):
        self.net = None
        self.level = level
        self.map_width = width
        self.map_length = length
        self.data = items.Data()
        self.maze = maze.Maze(self.data, width, length)
        self.run = True
        self.time = 0
        self.item = items.Exit([32 + 64 * random.randint(0, length - 1), 32 + 64 * random.randint(0, width - 1)])
        self.player = player.Player(32, 32, self.data, self.maze, self.item)
        self.player2 = player.Player(32 + 64 * (width - 1), 32 + 64 * (length - 1), self.data, self.maze, self.item)
        self.light_radius = 250
        self.torches = []
        self.compass = None
        self.compass_switch = False
        self.fog = pygame.Surface((1296, 720))
        self.connected = False

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
        for i in range(self.level + 6):
            if self.level > 1:
                lside = 8
            torch = items.Torch([32 + 64 * random.randint(0, side - 1) + 5, 32 + 64 * random.randint(0, lside - 1)])
            self.torches.append(torch)

    def spawn_torchesMulti(self):
        for i in range(1, 7):
            torch = items.Torch([32 + 64 * i, 32 + 64 * i])
            self.torches.append(torch)
        for j in range(1, 7):
            torch = items.Torch([32 + (64 * 2) + 64 * j, 32 + 64 * j])
            self.torches.append(torch)
        for k in range(1, 7):
            torch = items.Torch([32 + (64 * 4) + 64 * k, 32 + 64 * k])
            self.torches.append(torch)

    def redrawGameWindowForMulti(self):
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
        self.render_fog()
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

    def redrawGameWindowSingle(self):
        WINDOW.blit(BACKGROUND, [0, 0])
        for room in self.data.rooms:
            room.draw(WINDOW)
        self.item.draw(WINDOW)
        for torch in self.torches:
            torch.draw(WINDOW)
        if (self.level == 2 or self.level == 3) and self.compass is not None:
            self.compass.draw(WINDOW)
        self.player.draw(WINDOW)
        self.render_fog()
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
        if (self.level == 2 or self.level == 3) and self.compass is not None:
            if (self.player.x > self.compass.x + 16 or self.compass.x > self.player.x + 16) or (self.player.y > self.compass.y + 16 or self.compass.y > self.player.y + 16):
                pass
            else:
                self.compass = None
                self.compass_switch = True
        self.player.CheckForCollision(x, y)

    def increaseLevelForSingle(self):
        self.level += 1
        if self.level == 4:
            self.endStart()
        side = (self.level + 1) * 4
        lside = (self.level + 1) * 4
        if self.level > 1:
            lside = 8
        self.__init__(lside, side, self.level)
        if self.level == 3:
            self.item = items.Coin([32 + 64 * random.randint(0, side - 1), 32 + 64 * random.randint(0, lside - 1)])
            self.player = player.Player(32, 32, self.data, self.maze, self.item)
        self.startForSingle()

    def startForMulti(self):
        self.spawn_torchesMulti()
        self.maze.MazeSkeleton(0,0)
        self.maze.FillMaze()
        self.maze.ScrambleMaze()
        while self.run:
            self.time += 1
            CLOCK.tick(60)
            for event in pygame.event.get():
                if not pygame.mixer_music.get_busy():
                    filename = random.choice(MUSIC_LIST)
                    pygame.mixer_music.load(filename)
                    print(filename)
                    pygame.mixer_music.play(0)
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
            s = self.parse_data(self.send_data())
            self.player2.x, self.player2.y, self.player2.left, self.player2.right, self.player2.up, self.player2.down, self.player2.walk_count \
                = s[0:7]
            for torch in self.torches:
                if (self.player.x <= torch.x + 6 and torch.x <= self.player.x + 16 and self.player.y <= torch.y + 16 and \
                    torch.y <= self.player.y + 16):
                    self.torches.remove(torch)
                    self.light_radius += 150
            for torch in self.torches:
                if (
                        self.player2.x <= torch.x + 6 and torch.x <= self.player2.x + 16 and self.player2.y <= torch.y + 16 and \
                        torch.y <= self.player2.y + 16):
                    self.torches.remove(torch)
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
                self.endStart()
                self.player.x = 32
                self.player.y = 32
            WINDOW.fill((0, 0, 0))
            self.redrawGameWindowForMulti()

    def startForSingle(self):
        self.spawn_torches()
        self.maze.MazeSkeleton(0,0)
        self.maze.FillMaze()
        self.maze.ScrambleMaze()
        randomlist = list(range(0, 16))
        random.shuffle(randomlist)
        pygame.mixer_music.load(MUSIC_LIST[randomlist.pop()])
        pygame.mixer_music.set_volume(0.5)
        pygame.mixer_music.play(-1)
        if self.level == 2 or self.level == 3:
            side = (self.level + 1) * 4
            self.compass = items.Compass([32 + 64 * random.randint(0, 4 - 1)
                                          , 32 + 64 * random.randint(0, 4 - 1)])
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
            for torch in self.torches:
                if (self.player.x > torch.x + 6 or torch.x > self.player.x + 16 or self.player.y > torch.y + 16 or \
                    torch.y > self.player.y + 16):
                    pass
                else:
                    self.torches.remove(torch)
                    self.light_radius += 150
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
                self.increaseLevelForSingle()
            WINDOW.fill((0, 0, 0))
            self.redrawGameWindowSingle()

    def send_data(self):
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y) + "," + str(self.player.left) \
               + "," + str(self.player.right) + "," + str(self.player.up) + "," + str(self.player.down) + "," + str(self.player.walk_count)
        for torch in self.torches:
            data += "," + str(torch.x) + "," + str(torch.y)
        reply = self.net.send(data)
        return reply

    def parse_data(self, data):
        try:
            d = data.split(":")[1].split(",")
            d[0] = int(d[0])
            d[6] = int(d[6])
            d[1] = int(d[1])
            if d[2] == "False":
                d[2] = False
            elif d[2] == "True":
                d[2] = True
            if d[3] == "False":
                d[3] = False
            elif d[3] == "True":
                d[3] = True
            if d[4] == "False":
                d[4] = False
            elif d[4] == "True":
                d[4] = True
            if d[5] == "False":
                d[5] = False
            elif d[5] == "True":
                d[5] = True
            for i in range(7, len(d)):
                if d[i] == "False":
                    d[i] = False
                elif d[i] == "True":
                    d[i] = True
                else:
                    d[i] = int(d[i])
            return d
        except:
            return 0, 0, False, False, False, False, 0


    def menuStart(self):
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
            options = pygame.image.load('assets/2player.png')
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
                self.startForSingle()
                menu = False
            if 450 < x < 815 and 300 < y < 394 and mouse == 1:
                try:
                    self.__init__(8, 12, 0)
                    self.net = Network()
                    self.item = items.Coin(
                        [32 + 64 * (self.map_length - 1), 32 + 64 * (self.map_width - 1)])
                    self.player = player.Player(32, 32, self.data, self.maze, self.item)
                    self.startForMulti()
                    menu = False
                except:
                    my_font = pygame.font.SysFont('Comic Sans MS', 30)
                    text = my_font.render('Connection Not Found', True, (255, 0, 0))
                    WINDOW.blit(text, (500, 500))
            if 450 < x < 815 and 400 < y < 494 and mouse == 1:
                menu = False
            pygame.display.flip()
