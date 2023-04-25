

import sys
import random
import inspect
import math
import numpy as np
# from gamestate import GameState
# from cell import BaseCell
from collections import deque

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" %
          (method, line, fileName))
    sys.exit(1)


def flipCoin(p):
    r = random.random()
    return r < p


def BFS(cell, list, width, height):
    queue = deque()
    queue.append([(cell.x, cell.y)])

    explored = set()
    explored.add((cell.x, cell.y))

    while (queue):
        path = queue.pop()
        x, y = path[-1]
        for _cell in list: 
            if _cell.x == x and _cell.y == y: return path
        
        posPos = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        for _x, _y in posPos:
            if _x < 0 or _y < 0: posPos.remove((_x, _y))
            if _x >= width or _y >= height: posPos.remove((_x, _y))
        
        for pos in posPos:
            queue.append(path + [pos])
            explored.add(pos)


def nearestPoint(pos):
    """
    Finds the nearest grid point to a position (discretizes).
    """
    (current_row, current_col) = pos

    grid_row = int(current_row + 0.5)
    grid_col = int(current_col + 0.5)
    return (grid_row, grid_col)


def manhattanDistance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)



