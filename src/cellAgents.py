

import util
import random
import numpy as np


def NaiveUtility(action, cell, grid):
    neighbors = grid.getNeighbors(cell.x, cell.y)
    utility = 0
    if action == "ATTACK":
        for n in neighbors:
            if n.infected: utility += 1 * cell.attack_success
            else: utility -= 1 * cell.attack_success
    elif action == "MOVE":
        emptyNeigh = grid.getEmptyNeighbors(cell.x, cell.y)
        utility += len(emptyNeigh) / 5.
        if len(emptyNeigh)>0: pos = random.choice(emptyNeigh)
        else: pos = None
        return (utility, pos)
    else:
        return -np.inf
        """for n in neighbors:
            if n.infected: utility -= 1 * cell.attack_success
            else: utility += 1 * cell.attack_success"""
    return utility



def SmartUtility(action, cell, grid):
    neighbors = grid.getNeighbors(cell.x, cell.y, includeEmpty=1)
    nonEmpty = [neigh for neigh in neighbors if neigh is not None]
    closeLocal = grid.getLocalCells(cell.x, cell.y)

    MOVE_CONSTANT = 0.8

    utility = 0
    if action == "ATTACK":
        for i in nonEmpty:
            if i.infected: utility += 2.5 * cell.attack_success
            elif i.immune: utility -= 0.5 * cell.attack_success
            else: utility -= 1.5 * cell.attack_success

        closeImmune = [cell for cell in closeLocal if cell.immune]
        closeImmuneActivated = [cell for cell in closeImmune if cell.activated]
        utility += len(closeImmuneActivated) * 0.01
    elif action == "MOVE":
        distDict = {}

        closeInfected = [cell for cell in closeLocal if cell.infected]
        if len(closeInfected) == 0: return (0, (0,0))

        """
        closestPath = util.BFS(cell, closeInfected, grid.width, grid.height)

        if len(closestPath) > 1: return (MOVE_CONSTANT, closestPath[1])
        else: return (0, (0,0))
        """

        for n in closeInfected:
            neighs = grid.getNeighborPos(cell.x, cell.y)

            for newX, newY in neighs: distDict[(newX, newY)] = np.inf
            for newX, newY in neighs:
                dist = util.manhattanDistance((newX, newY), (n.x, n.y))
                if dist < distDict[(newX, newY)]: distDict[(newX, newY)] = dist
        if min(distDict.values()) == 0.0: return (0, (0,0))
        return (MOVE_CONSTANT * 1./min(distDict.values()), min(distDict, key=distDict.get))
    
    else: # for "PASS"
        return -np.inf
        """for n in nonEmpty:
            if n.infected: utility -= 1
            else: utility += 1"""
    return utility




def HelperUtility(action, cell, grid):
    localCells = grid.getLocalCells(cell.x, cell.y)
    numCells = len(localCells)
    numImmune = len([cell for cell in localCells if cell.immune])
    numInf = len([cell for cell in localCells if cell.infected])
    numHealthy = numCells - numImmune - numInf

    MOVE_CONSTANT = 0.05
    density = float(numCells) / float(grid.localRadius**2)

    # TODO incorporate % activated immune cells

    utility = 0

    if action == "ATTACK":
        if numCells>0: utility += (2.5* float(numInf) / float(numCells)) * density

    elif action == "PASS":
        if numCells>0: utility += (float(numHealthy) / float(numCells)) * density

    elif action == "MOVE":
        distDict = {}

        closeImmune = [cell for cell in localCells if cell.immune]
        if len(closeImmune) == 0: return (0, (0,0))

        """
        closestPath = util.BFS(cell, closeImmune, grid.width, grid.height)

        if len(closestPath) > 1: return (MOVE_CONSTANT, closestPath[1])
        else: return (0, (0,0))

        """
        for n in closeImmune:
            neighs = grid.getNeighborPos(cell.x, cell.y)

            for newX, newY in neighs: distDict[(newX, newY)] = np.inf
            for newX, newY in neighs:
                dist = util.manhattanDistance((newX, newY), (n.x, n.y))
                if dist < distDict[(newX, newY)]: distDict[(newX, newY)] = dist
        if min(distDict.values()) == 0.0: return (0, (0,0))
        return (MOVE_CONSTANT * 1./min(distDict.values()), min(distDict, key=distDict.get))

        
    return utility

    # if surrounded by healthy cells
        # boost reproductive probability

    # if surrounded by infected cells
        # boost immune cell reproductive probability
        # reduce infected probability