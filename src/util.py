

import sys
import random
import inspect
import math
import numpy as np
# from gamestate import GameState
# from cell import BaseCell

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



