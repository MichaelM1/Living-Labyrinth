import random
import items


class Maze(object):
    def __init__(self, data, map_width, map_length, grid_width, grid_length):
        self.grid = []
        self.stack = []
        self.visited = []
        self.radius = 64
        self.data = data
        self.dist = 32
        self.map_width = map_width
        self.map_length = map_length
        self.grid_width = grid_width
        self.grid_length = grid_length
        #self.test = []
        #self.testStr =[]

    def mazeSkeleton(self, x, y):
        temp = x
        for row in range(self.map_width):
            for col in range(self.map_length):
                if row == 0 or row == self.map_width - 1:
                    self.data.add(items.Wall((x, y)))
                    self.data.addString(str(items.Wall((x, y))))
                    #self.test.append(items.Wall((x, y)))
                    #self.testStr.append(str(items.Wall((x, y))))
                elif row % 4 == 0 and (col - 2) % 4 != 0:
                    self.data.add(items.Wall((x, y)))
                    self.data.addString(str(items.Wall((x, y))))
                    #self.test.append(items.Wall((x, y)))
                    #self.testStr.append(str(items.Wall((x, y))))
                elif row % 2 == 1 and col % 4 == 0:
                    self.data.add(items.Wall((x, y)))
                    self.data.addString(str(items.Wall((x, y))))
                    #self.test.append(items.Wall((x, y)))
                    #self.testStr.append(str(items.Wall((x, y))))
                elif (row - 2) % 4 == 0 and col == 0 or col == self.map_length - 1:
                    self.data.add(items.Wall((x, y)))
                    self.data.addString(str(items.Wall((x, y))))
                    #self.test.append(items.Wall((x, y)))
                    #self.testStr.append(str(items.Wall((x, y))))
                x += 16
            y += 16
            x = temp

    def fillMaze(self, x, y):
        temp = x
        for row in range(self.map_width):
            for col in range(self.map_length):
                if (row - 2) % 4 == 0 and col % 4 == 0 and col != 0 and col != self.map_length - 1:
                    i = 'Wall(' + str(x) + ',' + str(y) + ')'
                    if i not in self.data.wallsStr:
                        self.data.add(items.Wall((x, y)))
                        self.data.addString(str(items.Wall((x, y))))
                if row % 4 == 0 and (col - 2) % 4 == 0:
                    i = 'Wall(' + str(x) + ',' + str(y) + ')'
                    if i not in self.data.wallsStr:
                        self.data.add(items.Wall((x, y)))
                        self.data.addString(str(items.Wall((x, y))))
                x += 16
            y += 16
            x = temp

    def build_grid(self, x, y):
        temp = x
        for i in range(1, self.grid_width + 1):
            x = temp
            y = y + 64
            for j in range(1, self.grid_length + 1):
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

    def scrambleMaze(self, x, y):
        self.build_grid(x, -64 + y)
        self.stack.append((x, y))
        self.visited.append((x, y))
        while self.stack != []:
            cell = []
            if (x + self.radius, y) not in self.visited and (x + self.radius, y) in self.grid:
                cell.append(1)
            if (x - self.radius, y) not in self.visited and (x - self.radius, y) in self.grid:
                cell.append(2)
            if (x, y + self.radius) not in self.visited and (x, y + self.radius) in self.grid:
                cell.append(3)
            if (x, y - self.radius) not in self.visited and (x, y - self.radius) in self.grid:
                cell.append(4)
            if cell != []:
                cell_chosen = (random.choice(cell))
                if cell_chosen == 1:
                    self.right(x, y)
                    x = x + self.radius
                    self.visited.append((x, y))
                    self.stack.append((x, y))
                elif cell_chosen == 2:
                    self.left(x, y)
                    x = x - self.radius
                    self.visited.append((x, y))
                    self.stack.append((x, y))
                elif cell_chosen == 3:
                    self.down(x, y)
                    y = y + self.radius
                    self.visited.append((x, y))
                    self.stack.append((x, y))
                elif cell_chosen == 4:
                    self.up(x, y)
                    y = y - self.radius
                    self.visited.append((x, y))
                    self.stack.append((x, y))
            else:
                x, y = self.stack.pop()
        self.stack.clear()
        self.visited.clear()
        self.grid.clear()
