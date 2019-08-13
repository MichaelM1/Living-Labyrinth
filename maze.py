import random
import items

class Maze(object):
    def __init__(self, data, map_width, map_length):
        self.grid = []
        self.stack = []
        self.visited = []
        self.radius = 64
        self.data = data
        self.dist = 32
        self.map_width = map_width
        self.map_length = map_length

    def MazeSkeleton(self, x, y):
        temp = x
        self.data.rooms.clear()
        self.data.roomsStr.clear()
        for row in range(self.map_width):
            for col in range(self.map_length):
                self.data.Add(items.Room([row, col], x, y))
                self.data.AddString(str(items.Room([row, col], x, y)))
                x += 64
            y += 64
            x = temp

    def FillMaze(self):
        for room in self.data.rooms:
            room.right = True
            room.left = True
            room.up = True
            room.down = True

    def Up(self, pos):
        i = self.data.roomsStr.index('Room(' + str(pos[0]) + ',' + str(pos[1]) + ')')
        self.data.rooms[i].up = False
        j = self.data.roomsStr.index('Room(' + str(pos[0] - 1) + ',' + str(pos[1]) + ')')
        self.data.rooms[j].down = False

    def Down(self, pos):
        i = self.data.roomsStr.index('Room(' + str(pos[0]) + ',' + str(pos[1]) + ')')
        self.data.rooms[i].down = False
        j = self.data.roomsStr.index('Room(' + str(pos[0] + 1) + ',' + str(pos[1]) + ')')
        self.data.rooms[j].up = False

    def Left(self, pos):
        i = self.data.roomsStr.index('Room(' + str(pos[0]) + ',' + str(pos[1]) + ')')
        self.data.rooms[i].left = False
        j = self.data.roomsStr.index('Room(' + str(pos[0]) + ',' + str(pos[1] - 1) + ')')
        self.data.rooms[j].right = False

    def Right(self, pos):
        i = self.data.roomsStr.index('Room(' + str(pos[0]) + ',' + str(pos[1]) + ')')
        self.data.rooms[i].right = False
        j = self.data.roomsStr.index('Room(' + str(pos[0]) + ',' + str(pos[1] + 1) + ')')
        self.data.rooms[j].left = False

    def BuildGrid(self):
        for row in range(self.map_width):
            for col in range(self.map_length):
                self.grid.append([row, col])

    def ScrambleMaze(self):
            x = y = 0
            self.BuildGrid()
            self.stack.append([x, y])
            self.visited.append([x, y])
            while self.stack != []:
                cell = []
                if [x, y + 1] not in self.visited and [x, y + 1] in self.grid:
                    cell.append(1)
                if [x, y - 1] not in self.visited and [x, y - 1] in self.grid:
                    cell.append(2)
                if [x + 1, y] not in self.visited and [x + 1, y] in self.grid:
                    cell.append(3)
                if [x - 1, y] not in self.visited and [x - 1, y] in self.grid:
                    cell.append(4)
                if cell != []:
                    cell_chosen = (random.choice(cell))
                    if cell_chosen == 1:
                        self.Right([x, y])
                        y = y + 1
                        self.visited.append([x, y])
                        self.stack.append([x, y])
                    elif cell_chosen == 2:
                        self.Left([x, y])
                        y = y - 1
                        self.visited.append([x, y])
                        self.stack.append([x, y])
                    elif cell_chosen == 3:
                        self.Down([x, y])
                        x = x + 1
                        self.visited.append([x, y])
                        self.stack.append([x, y])
                    elif cell_chosen == 4:
                        self.Up([x, y])
                        x = x - 1
                        self.visited.append([x, y])
                        self.stack.append([x, y])
                else:
                    j = self.stack.pop()
                    x = j[0]
                    y = j[1]
            self.stack.clear()
            self.visited.clear()
            self.grid.clear()
