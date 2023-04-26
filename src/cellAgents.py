

import util
import random
import numpy as np


def NaiveUtility(cell, localCells, localArea):

    utilDict = {}
    utilDict["ATTACK"] = 0.
    utilDict["MOVE"] = 0.
    utilDict["PASS"] = 0.

    density = float(len(localCells)) / float(localArea)

    # ATTACK
    if cell.helper:
        for n in localCells:
            if n.infected or n.immune: utilDict["ATTACK"] += 1 * cell.helper_boost
            else: utilDict["ATTACK"] -= 1 * cell.helper_boost
    else:
        for n in localCells:
            if n.infected: utilDict["ATTACK"] += 1 * cell.attack_success
            else: utilDict["ATTACK"] -= 1 * cell.attack_success

    # MOVE
    if cell.helper:
        if density < 1./(1. + cell.helper_boost): utilDict["MOVE"] += 1.5 * cell.helper_boost

    else:
        if density < 0.35: utilDict["MOVE"] += 1.5 * cell.attack_success
    
    # PASS
    utilDict["PASS"] = -np.inf # no passing if naive

    return max(utilDict, key=utilDict.get) # return action with maximum utility




def SmartUtility(cell, localCells, localArea):

    MOVE_CONSTANT = 0.8

    utilDict = {}
    utilDict["ATTACK"] = 0.
    utilDict["MOVE"] = 0.
    utilDict["PASS"] = 0.

    density = float(len(localCells)) / float(localArea)

    numCells = len(localCells)
    numImmune = len([cell for cell in localCells if cell.immune])
    numInf = len([cell for cell in localCells if cell.infected])
    numHealthy = numCells - numImmune - numInf


    # ATTACK
    if cell.helper:
        if numCells>0: utilDict["ATTACK"] += (2.5* float(numInf) / float(numCells)) * density

    else:
        for i in localCells:
            if i.infected: utilDict["ATTACK"] += 2.5 * cell.attack_success
            elif i.immune: utilDict["ATTACK"] -= 0.5 * cell.attack_success
            else: utilDict["ATTACK"] -= 1.5 * cell.attack_success

    # MOVE
    if cell.helper:
        utilDict["MOVE"] += (float(numImmune) / float(numCells))

    else:

        utilDict["MOVE"] += (float(numHealthy) - float(numInf) / float(numCells))
    
    # "PASS"
    if cell.helper:
        if numCells>0: utilDict["PASS"] += (float(numHealthy) / float(numCells)) * density
    
    else:
        utilDict["PASS"] += -np.inf

    
    return max(utilDict, key=utilDict.get) # return action with maximum utility
