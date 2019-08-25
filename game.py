import math
import random
import pygame
import items
import maze
import player

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer_music.set_volume(0.5)
WINDOW = pygame.display.set_mode((1296, 720))
pygame.display.set_caption("Living Labyrinth")
CLOCK = pygame.time.Clock()
BACKGROUND = pygame.image.load('assets/background.jpg').convert()
MENU_SCREEN = pygame.image.load('assets/menuScreen.png').convert()
START_BUTTON = pygame.image.load('assets/start.PNG').convert()
END_SCREEN = pygame.image.load('assets/end.jpg').convert()
WIN_SCREEN = pygame.image.load('assets/end2.jpg').convert()
justplayed = None
MUSIC_LIST = ['Sound/Aria Math.mp3', 'Sound/Beginning 2.mp3', 'Sound/Clark.mp3'
              , 'Sound/Danny.mp3', 'Sound/Dreiton.mp3', 'Sound/Dry Hands.mp3'
              , 'Sound/Haggstrom.mp3', 'Sound/Haunt Muskie.mp3', 'Sound/Living Mice.mp3'
              , 'Sound/Mice On Venus.mp3', 'Sound/Moog City 2.mp3', 'Sound/Mutation.mp3'
              , 'Sound/Subwoofer Lullaby.mp3', 'Sound/Sweden.mp3', 'Sound/Taswell.mp3'
              , 'Sound/Wet Hands.mp3']


class Game(object):
    def __init__(self, width, length, level):
        self.level = level
        self.map_width = width
        self.map_length = length
        self.data = items.Data()
        self.maze = maze.Maze(self.data, width, length)
        self.multi = False
        self.run = True
        self.time = 0
        self.item = items.Exit([32 + 64 * random.randint(length//2 - 1, length//2 + 1), 32 + 64 * random.randint(width//2 - 1, width//2 + 1)])
        self.player = player.Player(32, 32, self.data, self.maze, self.item)
        self.player2 = player.Player(32 + 64 * (length - 1), 32 + 64 * (width - 1), self.data, self.maze, self.item)
        self.light_radius = 250
        self.light_radius_player2 = 250
        self.torches = []
        self.boots = []
        self.compass = None
        self.compass_switch = False
        self.fog = pygame.Surface((1296, 720))
        self.movespeed_player2 = 3
        self.movespeed = 3

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
            WINDOW.blit(WIN_SCREEN, [0, 0])
            pygame.display.flip()

    def gameOver(self):
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
        self.fog.fill((0, 0, 0))
        self.light_rect.center = (self.player.x + 8, self.player.y + 8)
        self.fog.blit(self.light_mask, self.light_rect)
        if self.multi:
            self.light_rect2.center = (self.player2.x + 8, self.player2.y + 8)
            self.fog.blit(self.light_mask2, self.light_rect2)
        WINDOW.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)

    def spawn_boots(self):
        side = (self.level + 1) * 4
        lside = (self.level + 1) * 4
        for i in range(1):
            if self.level > 1:
                lside = 8
            boots = items.Boots([32 + 64 * random.randint(0, side - 1) + 5, 32 + 64 * random.randint(0, lside - 1)])
            self.boots.append(boots)

    def spawn_torches(self):
        side = (self.level + 1) * 4
        lside = (self.level + 1) * 4
        for i in range(self.level + 6):
            if self.level > 1:
                lside = 8
            torch = items.Torch([32 + 64 * random.randint(0, side - 1) + 5, 32 + 64 * random.randint(0, lside - 1)])
            self.torches.append(torch)

    def redrawGameWindowMulti(self):
        WINDOW.blit(BACKGROUND, [0, 0])
        for room in self.data.rooms:
            room.draw(WINDOW)
        self.item.draw(WINDOW)
        for boot in self.boots:
            boot.draw(WINDOW)
        for torch in self.torches:
            torch.draw(WINDOW)
        if (self.level == 2 or self.level == 3) and self.compass is not None:
            self.compass.draw(WINDOW)
        self.player.draw(WINDOW)
        self.player2.draw(WINDOW)
        self.render_fog()
        if self.compass_switch:
            disx = self.item.x - self.player.x
            if disx == 0:
                disx = 1
            disy = self.item.y - self.player.y
            radian = math.atan(disy / disx)
            degree = -(radian * (180 / math.pi))
            if disx < 0 < disy:
                degree = -180 + degree
            if disx < 0 and disy < 0:
                degree = 180 + degree
            degree = degree * (math.pi / 180)
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
        for boot in self.boots:
            boot.draw(WINDOW)
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
            radian = math.atan(disy / disx)
            degree = -(radian * (180 / math.pi))
            if disx < 0 and disy > 0:
                degree = -180 + degree
            if disx < 0 and disy < 0:
                degree = 180 + degree
            degree = degree * (math.pi / 180)
            x1 = math.cos(degree) * 40
            y1 = math.sin(degree) * -40
            pygame.draw.circle(WINDOW, (105, 105, 105), (1000, 500), 50)
            pygame.draw.circle(WINDOW, (0, 0, 0), (1000, 500), 45)
            pygame.draw.line(WINDOW, (255, 0, 0), (1000, 500), (1000 + x1, 500 + y1), 1)
        pygame.display.flip()

    def update(self, x, y):
        col = (self.player.x - 14) // 64
        row = (self.player.y - 14) // 64
        if 16 + 64 * col < self.player.x < 48 + 64 * col and 16 + 64 * row < self.player.y < 48 + 64 * row and abs(
                self.player.col - col) + abs(self.player.row - row) > 5:
            col1 = (self.player2.x - 14) // 64
            row1 = (self.player2.y - 14) // 64
            if 16 + 64 * col1 < self.player2.x < 48 + 64 * col1 and 16 + 64 * row1 < self.player2.y < 48 + 64 * row1:
                self.player.row = row
                self.player.col = col
                self.player.maze.FillMaze()
                self.player.maze.ScrambleMaze()
        for torch in self.torches:
            if (self.player.x > torch.x + 6 or torch.x > self.player.x + 16 or self.player.y > torch.y + 16 or \
                    torch.y > self.player.y + 16):
                pass
            else:
                self.torches.remove(torch)
                self.light_radius += 150
        self.player.move(x, y)
        if (self.level == 2 or self.level == 3) and self.compass is not None:
            if (self.player.x > self.compass.x + 16 or self.compass.x > self.player.x + 16) or (
                    self.player.y > self.compass.y + 16 or self.compass.y > self.player.y + 16):
                pass
            else:
                self.compass = None
                self.compass_switch = True
        self.player.checkForCollision(x, y)

    def update_player2(self, x, y):
        col = (self.player2.x - 14) // 64
        row = (self.player2.y - 14) // 64
        if 16 + 64 * col < self.player2.x < 48 + 64 * col and 16 + 64 * row < self.player2.y < 48 + 64 * row and abs(
                self.player2.col - col) + abs(self.player2.row - row) > 5:
            col1 = (self.player.x - 14) // 64
            row1 = (self.player.y - 14) // 64
            if 16 + 64 * col1 < self.player.x < 48 + 64 * col1 and 16 + 64 * row1 < self.player.y < 48 + 64 * row1:
                self.player2.row = row
                self.player2.col = col
                self.player2.maze.FillMaze()
                self.player2.maze.ScrambleMaze()
        for torch in self.torches:
            if (self.player2.x > torch.x + 6 or torch.x > self.player2.x + 16 or self.player2.y > torch.y + 16 or \
                    torch.y > self.player2.y + 16):
                pass
            else:
                self.torches.remove(torch)
                self.light_radius_player2 += 150
        self.player2.move(x, y)
        if (self.level == 2 or self.level == 3) and self.compass is not None:
            if (self.player2.x > self.compass.x + 16 or self.compass.x > self.player2.x + 16) or (
                    self.player2.y > self.compass.y + 16 or self.compass.y > self.player2.y + 16):
                pass
            else:
                self.compass = None
                self.compass_switch = True
        self.player2.checkForCollision(x, y)

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

    def increaseLevelForMulti(self):
        self.level += 1
        if self.level == 4:
            self.endStart()
        side = (self.level + 1) * 4
        lside = (self.level + 1) * 4
        if self.level > 1:
            lside = 8
        self.__init__(lside, side, self.level)
        self.multi = True
        if self.level == 3:
            self.item = items.Coin([32 + 64 * random.randint(0, side - 1), 32 + 64 * random.randint(0, lside - 1)])
            self.player = player.Player(32, 32, self.data, self.maze, self.item)
            self.player2 = player.Player(32 + 64 * (self.map_length - 1), 32 + 64 * (self.map_width - 1), self.data, self.maze, self.item)
        self.start_multi()

    def startForSingle(self):
        global justplayed
        self.spawn_torches()
        self.spawn_boots()
        self.maze.MazeSkeleton(0, 0)
        self.maze.FillMaze()
        self.maze.ScrambleMaze()
        while self.run:
            self.time += 1
            CLOCK.tick(60)
            for event in pygame.event.get():
                if not pygame.mixer_music.get_busy():
                    filename = random.choice(MUSIC_LIST)
                    while filename == justplayed:
                        filename = random.choice(MUSIC_LIST)
                    justplayed = filename
                    pygame.mixer_music.load(filename)
                    print(filename)
                    pygame.mixer_music.play(0)
                if event.type == pygame.QUIT:
                    self.run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.update(self.movespeed, 0)
                self.player.left = True
                self.player.right = False
                self.player.up = False
                self.player.down = False
            if keys[pygame.K_RIGHT]:
                self.update(-self.movespeed, 0)
                self.player.left = False
                self.player.right = True
                self.player.up = False
                self.player.down = False
            if keys[pygame.K_UP]:
                self.update(0, self.movespeed)
                self.player.left = False
                self.player.right = False
                self.player.up = True
                self.player.down = False
            if keys[pygame.K_DOWN]:
                self.update(0, -self.movespeed)
                self.player.left = False
                self.player.right = False
                self.player.up = False
                self.player.down = True
            if keys[pygame.K_q]:
                self.run = False
            for boot in self.boots:
                if (self.player.x <= boot.x + 16 and boot.x <= self.player.x + 16 and self.player.y <= boot.y + 16 and
                        boot.y <= self.player.y + 16):
                    self.boots.remove(boot)
                    self.movespeed += 1
            if self.time // 5 == 1:
                self.time = 0
                self.light_radius -= 1
                if self.light_radius == 0:
                    self.gameOver()
            self.fog.fill((20, 20, 20))
            self.light_mask = pygame.image.load(('assets/light_mask.png')).convert_alpha()
            self.light_mask = pygame.transform.scale(self.light_mask, (self.light_radius, self.light_radius))
            self.light_rect = self.light_mask.get_rect()
            if self.player.end:
                self.increaseLevelForSingle()
            WINDOW.fill((0, 0, 0))
            self.redrawGameWindowSingle()

    def start_multi(self):
        global justplayed
        self.spawn_torches()
        self.spawn_boots()
        self.maze.MazeSkeleton(0, 0)
        self.maze.FillMaze()
        self.maze.ScrambleMaze()
        if self.level == 2 or self.level == 3:
            side = (self.level + 1) * 4
            self.compass = items.Compass([32 + 64 * random.randint(0, 4 - 1),
                                          32 + 64 * random.randint(0, 4 - 1)])
        while self.run:
            self.time += 1
            CLOCK.tick(60)
            for event in pygame.event.get():
                if not pygame.mixer_music.get_busy():
                    filename = random.choice(MUSIC_LIST)
                    while filename == justplayed:
                        filename = random.choice(MUSIC_LIST)
                    justplayed = filename
                    pygame.mixer_music.load(filename)
                    print(filename)
                    pygame.mixer_music.play(0)
                if event.type == pygame.QUIT:
                    self.run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.update(self.movespeed, 0)
                self.player.left = True
                self.player.right = False
                self.player.up = False
                self.player.down = False
            if keys[pygame.K_a]:
                self.update_player2(self.movespeed_player2, 0)
                self.player2.left = True
                self.player2.right = False
                self.player2.up = False
                self.player2.down = False
            if keys[pygame.K_RIGHT]:
                self.update(-self.movespeed, 0)
                self.player.left = False
                self.player.right = True
                self.player.up = False
                self.player.down = False
            if keys[pygame.K_d]:
                self.update_player2(-self.movespeed_player2, 0)
                self.player2.left = False
                self.player2.right = True
                self.player2.up = False
                self.player2.down = False
            if keys[pygame.K_UP]:
                self.update(0, self.movespeed)
                self.player.left = False
                self.player.right = False
                self.player.up = True
                self.player.down = False
            if keys[pygame.K_w]:
                self.update_player2(0, self.movespeed_player2)
                self.player2.left = False
                self.player2.right = False
                self.player2.up = True
                self.player2.down = False
            if keys[pygame.K_DOWN]:
                self.update(0, -self.movespeed)
                self.player.left = False
                self.player.right = False
                self.player.up = False
                self.player.down = True
            if keys[pygame.K_s]:
                self.update_player2(0, -self.movespeed_player2)
                self.player2.left = False
                self.player2.right = False
                self.player2.up = False
                self.player2.down = True
            if keys[pygame.K_q]:
                self.run = False
            for boot in self.boots:
                if (self.player.x > boot.x + 16 or boot.x > self.player.x + 16 or self.player.y > boot.y + 16 or
                        boot.y > self.player.y + 16):
                    pass
                else:
                    self.boots.remove(boot)
                    self.movespeed += 1
                if (self.player2.x > boot.x + 16 or boot.x > self.player2.x + 16 or self.player2.y > boot.y + 16 or
                        boot.y > self.player2.y + 16):
                    pass
                else:
                    self.boots.remove(boot)
                    self.movespeed_player2 += 1
            if self.time // 5 == 1:
                self.time = 0
                if self.light_radius != 0:
                    self.light_radius -= 1
                if self.multi and self.light_radius_player2 != 0:
                    self.light_radius_player2 -= 1
                if self.light_radius == 0 and self.light_radius_player2 == 0:
                    self.gameOver()
            self.fog.fill((20, 20, 20))
            self.light_mask = pygame.image.load(('assets/light_mask.png')).convert_alpha()
            self.light_mask = pygame.transform.scale(self.light_mask, (self.light_radius, self.light_radius))
            self.light_mask2 = pygame.transform.scale(self.light_mask, (self.light_radius_player2, self.light_radius_player2))
            self.light_rect = self.light_mask.get_rect()
            self.light_rect2 = self.light_mask2.get_rect()
            if self.player.end or self.player2.end:
                self.increaseLevelForMulti()
            WINDOW.fill((0, 0, 0))
            self.redrawGameWindowMulti()

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
                self.multi = True
                self.start_multi()
                menu = False
            if 450 < x < 815 and 400 < y < 494 and mouse == 1:
                menu = False
            pygame.display.flip()
