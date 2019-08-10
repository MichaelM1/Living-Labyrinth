import wall
import random


class Maze(object):

    def __init__(self, data):
        self.grid = []
        self.stack = []
        self.visited = []
        self.radius = 64
        self.data = data
        self.dist = 32

    def fillMaze(self):
        x = y = 0
        for row in range(29):
            for col in range(41):
                if (row - 2) % 4 == 0 and col % 4 == 0 and col != 0 and col != 40:
                    i = 'Wall(' + str(x) + ',' + str(y) + ')'
                    if i not in self.data.wallsStr:
                        self.data.add(wall.Wall((x, y)))
                        self.data.addString(str(wall.Wall((x, y))))
                if row % 4 == 0 and (col - 2) % 4 == 0:
                    i = 'Wall(' + str(x) + ',' + str(y) + ')'
                    if i not in self.data.wallsStr:
                        self.data.add(wall.Wall((x, y)))
                        self.data.addString(str(wall.Wall((x, y))))
                x += 16
            y += 16
            x = 0

    def build_grid(self, x, y):
        for i in range(1, 8):
            x = 32
            y = y + 64
            for j in range(1, 11):
                self.grid.append((x, y))
                x = x + 64

    def up(self, x, y):
        y = y - self.dist
        i = self.data.wallsStr.index('Wall(' + str(x) + ',' + str(y) + ')')
        del self.data.walls[i]
        del self.data.wallsStr[i]

    def down(self, x, y):
        y = y + self.dist
        i = self.data.wallsStr.index('Wall(' + str(x) + ',' + str(y) + ')')
        del self.data.walls[i]
        del self.data.wallsStr[i]

    def left(self, x, y):
        x = x - self.dist
        i = self.data.wallsStr.index('Wall(' + str(x) + ',' + str(y) + ')')
        del self.data.walls[i]
        del self.data.wallsStr[i]

    def right(self, x, y):
        x = x + self.dist
        i = self.data.wallsStr.index('Wall(' + str(x) + ',' + str(y) + ')')
        del self.data.walls[i]
        del self.data.wallsStr[i]

    def scrambleMaze(self, x=32, y=32):
        self.build_grid(32, -32)
        self.stack.append((x, y))
        self.visited.append((x, y))
        while len(self.stack) > 0:
            cell = []
            if (x + self.radius, y) not in self.visited and (x + self.radius, y) in self.grid:
                cell.append("right")
            if (x - self.radius, y) not in self.visited and (x - self.radius, y) in self.grid:
                cell.append("left")
            if (x, y + self.radius) not in self.visited and (x, y + self.radius) in self.grid:
                cell.append("down")
            if (x, y - self.radius) not in self.visited and (x, y - self.radius) in self.grid:
                cell.append("up")
            if len(cell) > 0:
                cell_chosen = (random.choice(cell))
                if cell_chosen == "right":
                    self.right(x, y)
                    x = x + self.radius
                    self.visited.append((x, y))
                    self.stack.append((x, y))
                elif cell_chosen == "left":
                    self.left(x, y)
                    x = x - self.radius
                    self.visited.append((x, y))
                    self.stack.append((x, y))
                elif cell_chosen == "down":
                    self.down(x, y)
                    y = y + self.radius
                    self.visited.append((x, y))
                    self.stack.append((x, y))
                elif cell_chosen == "up":
                    self.up(x, y)
                    y = y - self.radius
                    self.visited.append((x, y))
                    self.stack.append((x, y))
            else:
                x, y = self.stack.pop()
        self.stack.clear()
        self.visited.clear()
