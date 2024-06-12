

import sys
import random
import inspect
import math
import numpy as np
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
    # TODO update to rely on not cells or move to another file that can import BaseCell
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


def isNeighbor(x1, y1, x2, y2):
    return (x1==x2 and abs(y1-y2)==1) or (y1==y2 and abs(x1-x2)==1)


def getNeighboringPositions(x, y, width, height):
    neighbors = []
    if y+1 < height:
        neighbors.append((x, y+1))
    if y-1 >= 0:
        neighbors.append((x, y-1))
    if x+1 < width:
        neighbors.append((x-1, y))
    if x-1 >= 0:
        neighbors.append((x+1, y))
    return neighbors


def removeIndexesFromList(testListToModify, idxToRemoveList):
    res = []
    for idx, ele in enumerate(testListToModify): 
        # checking if element not present in index list
        if idx not in idxToRemoveList:
            res.append(ele)
    return res

def addItemAtIndexesToList(listToModify: list[any], idxToAddList: list[int], itemToAdd):
    idxToAddList.sort()
    for _idx in idxToAddList:
        assert _idx <= len(listToModify) # is this necessary?
        listToModify.insert(_idx, itemToAdd)
    return listToModify

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



