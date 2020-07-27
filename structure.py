import math
import random
import pygame

class Cell:
    def __init__(self, x, y, block_size):
        self.x = x
        self.y = y
        self.block_size = block_size
        self.visited = False
        self.distance = math.inf
        self.edgeWeight = 1
        self.predecessor = None
        self.startFlag = False
        self.destFlag = False
        self.pathFlag = False
        self.wallFlag = False

    def drawCell(self, win):
        if self.visited:
            self.draw(win, (88, 107, 214))
        else:
            self.draw(win, (100, 100, 100))
            if self.edgeWeight == 2:
                self.draw(win, (168, 127, 50))

            if self.edgeWeight == 3:
                self.draw(win, (50, 168, 62))

        if self.startFlag:
            self.draw(win, (59, 126, 235))

        if self.destFlag:
            self.draw(win, (245, 66, 96))

        if self.pathFlag and not self.destFlag:
            self.draw(win, (234, 247, 82))

        if self.wallFlag and (not self.startFlag or not self.destFlag):
            self.draw(win, (0, 0, 0))

    def setWallFlag(self):
        self.wallFlag = True

    def draw(self, win, color):
        pygame.draw.rect(win, color, [self.x * self.block_size, self.y * self.block_size, self.block_size, self.block_size])
        pygame.draw.rect(win, (0, 0, 0), [self.x * self.block_size, self.y * self.block_size, self.block_size, self.block_size], 1)



class Grid:

    def __init__(self, width, height, block_size):
        self.cellList = []
        self.width = width
        self.height = height
        self.block_size = block_size
        self.columns = math.floor(height / block_size)
        self.rows = math.floor(width / block_size)

    def initGrid(self):
        for y in range(self.rows):
            for x in range(self.columns):
                self.cellList.append(Cell(x, y, self.block_size))

    def getCellList(self):
        return self.cellList

    def getRandomCell(self):
        return self.cellList[random.randint(0, len(self.cellList) - 1)]

    def checkNeighbours(self, cell):
        neighbours = []

        cellTop = self.getCell(self.getIndex(cell.x, cell.y - 1))
        cellRight = self.getCell(self.getIndex(cell.x + 1, cell.y))
        cellBottom = self.getCell(self.getIndex(cell.x, cell.y + 1))
        cellLeft = self.getCell(self.getIndex(cell.x - 1, cell.y))

        if cellTop is not None and not cellTop.visited and not cellTop.wallFlag:
            neighbours.append(cellTop)
        if cellRight is not None and not cellRight.visited and not cellRight.wallFlag:
            neighbours.append(cellRight)
        if cellBottom is not None and not cellBottom.visited and not cellBottom.wallFlag:
            neighbours.append(cellBottom)
        if cellLeft is not None and not cellLeft.visited and not cellLeft.wallFlag:
            neighbours.append(cellLeft)

        return neighbours

    def getAllNeighbours(self):
        allNeighbours = []

        for cell in self.cellList:
            allNeighbours.extend(self.checkNeighbours(cell))

        return allNeighbours

    def makeNoise(self):
        for cell in self.cellList:
            if cell.destFlag or cell.startFlag:
                pass
            else:
                if random.random() < 0.2:
                    cell.edgeWeight = random.randint(2, 3)


    def getIndex(self, x, y):
        index = None
        if x < 0 or x > self.columns - 1 or y < 0 or y > self.rows - 1:
            index = -1
            return -1

        index = x + y * self.columns
        return index


    def getCell(self, index):
        cell = None

        if not index == -1:
            cell = self.cellList[index]

        return cell