import math
import random
import pygame
import items
import maze
import player
import game

data1 = items.Data()
maze1 = maze.Maze(data1, 4, 4)
exit1 = items.Exit([32 + 64 * random.randint(0, 4 - 1), 32 + 64 * random.randint(0, 4 - 1)])
player1 = player.Player(32, 32, data1, maze1, exit1)
game1 = game.Game(4, 4, maze1, exit1, data1, player1, 0)
game.menuStart()