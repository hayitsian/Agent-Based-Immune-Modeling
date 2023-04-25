

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
                    dist = util.manhattanDistance((newX, newY), (n.x, n.y))
                    if dist < distDict[(newX, newY)]: distDict[(newX, newY)] = dist
            else: return (0, (0,0))

        return (0.8, min(distDict, key=distDict.get))
    
    else: # for "PASS"
        for n in nonEmpty:
            if n.infected: utility -= 1
            else: utility += 1
    return utility




def HelperUtility(action, cell, grid):
    localCells = grid.getLocalCells(cell.x, cell.y)
    numCells = len(localCells)
    numImmune = len([cell for cell in localCells if cell.immune])
    numInf = len([cell for cell in localCells if cell.infected])
    numHealthy = numCells - numImmune - numInf

    MOVE_CONSTANT = 2.
    density = numCells / (grid.localRadius**2)

    # TODO incorporate % activated immune cells

    utility = 0

    if action == "ATTACK":
        if numCells>0: utility += (numCells - numHealthy) / float(numCells) * density

    elif action == "PASS":
        if numCells>0: utility += (numHealthy) / float(numCells) * density

    elif action == "MOVE":
        densDict = {}
        emptyNeigh = grid.getEmptyNeighbors(cell.x, cell.y)
        if len(emptyNeigh) > 0:
            for newX, newY in emptyNeigh: densDict[(newX, newY)] = 0
            for newX, newY in emptyNeigh:
                numLocalCells = len(grid.getLocalCells(newX, newY))
                dens = numLocalCells / grid.localRadius**2
                if dens > densDict[(newX, newY)]: densDict[(newX, newY)] = dens
            pos = max(densDict, key=densDict.get)
            diff = densDict[pos] - density
            return (diff * MOVE_CONSTANT, pos)
        else: return (0, (0,0))

    return utility

    # if surrounded by healthy cells
        # boost reproductive probability

    # if surrounded by infected cells
        # boost immune cell reproductive probability
        # reduce infected probability