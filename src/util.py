

import sys
import random
import inspect
import math
import numpy as np

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



def NaiveUtility(action, cell, grid):
    neighbors = grid.getNeighbors(cell.x, cell.y)
    utility = 0
    if action == "ATTACK":
        for n in neighbors:
            if n.infected: utility += 1 * cell.attack_success
            else: utility -= 1 * cell.attack_success
    else:
        for n in neighbors:
            if n.infected: utility -= 1 * cell.attack_success
            else: utility += 1 * cell.attack_success
    return utility



def SmartUtility(action, cell, grid):
    neighbors = grid.getNeighbors(cell.x, cell.y, includeEmpty=1)
    nonEmpty = [neigh for neigh in neighbors if neigh is not None]
    closeLocal = grid.getLocalCells(cell.x, cell.y)
    utility = 0
    if action == "ATTACK":
        for n in nonEmpty:
            if n.infected: utility += 1 * cell.attack_success
            elif n.immune: utility -= 0.5 * cell.attack_success
            else: utility -= 1.5 * cell.attack_success
        closeImmune = [cell for cell in closeLocal if cell.immune]
        closeImmuneActivated = [cell for cell in closeImmune if cell.activated]
        utility += len(closeImmuneActivated) * 0.03
    elif action == "MOVE":
        distDict = {}

        closeInfected = [cell for cell in closeLocal if cell.infected]
        if len(closeInfected) == 0: return (0, (0,0))
        for n in closeInfected:
            emptyNeigh = grid.getEmptyNeighbors(cell.x, cell.y)
            if len(emptyNeigh) > 0:
                for newX, newY in emptyNeigh: distDict[(newX, newY)] = np.inf
                for newX, newY in emptyNeigh:
                    dist = manhattanDistance((newX, newY), (n.x, n.y))
                    if dist < distDict[(newX, newY)]: distDict[(newX, newY)] = dist
            else: return (0, (0,0))

        return (0.8, min(distDict, key=distDict.get))
    
    else: # for "PASS"
        for n in nonEmpty:
            if n.infected: utility -= 1
            else: utility += 1
    return utility