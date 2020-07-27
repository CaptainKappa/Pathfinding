import math
import pygame
import dijkstra as d

from structure import Grid


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BLOCK_SIZE = 25
COLUMNS = math.floor(WINDOW_WIDTH / BLOCK_SIZE)
ROWS = math.floor(WINDOW_WIDTH / BLOCK_SIZE)

def drawDisplay(win, grid):
    for i in range(len(grid)):
        grid[i].drawCell(win)
    pygame.display.update()


def drawPath(win, path):
    for i in range(len(path)):
        path[i].drawCell(win)
    pygame.display.update()


def getPath(destination):
    current = destination
    path = []

    while current.predecessor is not None:
        current.pathFlag = True
        path.append(current)
        current = current.predecessor

    path.reverse()
    return path


def main():
    pygame.init()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    grid = Grid(WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE)
    grid.initGrid()

    initial = grid.getRandomCell()
    initial.startFlag = True
    initial.distance = 0

    destination = grid.getRandomCell()
    destination.destFlag = True

    current = initial

    grid.makeNoise()

    running = True
    wallLoop = True
    motion = False

    while running:
        clock.tick(60)
        # optional setting walls before path finding
        while wallLoop:
            drawDisplay(win, grid.getCellList())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    motion = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    motion = False
                elif event.type == pygame.MOUSEMOTION:
                    if motion:
                        mouseX, mouseY = pygame.mouse.get_pos()
                        grid.cellList[grid.getIndex(int(mouseX / BLOCK_SIZE), int(mouseY / BLOCK_SIZE))].setWallFlag()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        wallLoop = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

        # end condition
        if destination.visited:
            print(destination.distance)
            drawPath(win, getPath(destination))

            running = False

        # use dijkstra algorithm to get next cell
        current, grid.cellList = d.solve(current, grid)
        drawDisplay(win, grid.getCellList())
    #quit()


main()