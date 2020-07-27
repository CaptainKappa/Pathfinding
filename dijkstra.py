import math

def solve(current, grid):
    neighbours = grid.checkNeighbours(current)

    for neighbour in neighbours:
        tentDist = current.distance + neighbour.edgeWeight
        if tentDist < neighbour.distance:
            neighbour.distance = tentDist
            neighbour.predecessor = current

    # 4
    current.visited = True

    tempDist = math.inf
    for cell in grid.getAllNeighbours():
        if not cell.visited:
            if cell.distance < tempDist:
                tempDist = cell.distance
                current = cell

    return current, grid.cellList

