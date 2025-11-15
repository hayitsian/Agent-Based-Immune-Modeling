

import util
import random
import numpy as np

def StupidUtility(cell, localCells, localArea):
    utilDict = {}
    utilDict["ATTACK"] = 0.
    utilDict["MOVE"] = 0.
    utilDict["PASS"] = 0.

    if (len([cell for cell in localCells if cell.infected]) > 0):
        utilDict["ATTACK"] = 100000000.
    else: utilDict["MOVE"] = 100000000.

    return max(utilDict, key=utilDict.get), utilDict # return action with maximum utility

def NaiveUtility(cell, localCells, localArea):

    utilDict = {}
    utilDict["ATTACK"] = 0.
    utilDict["MOVE"] = 0.
    utilDict["PASS"] = 0.

    numCells = len(localCells)

    density = 0.0
    hlpDense = 0.0
    immDensity = 0.0

    if numCells > 0: 
        density = float(numCells) / float(localArea)
        hlpDense = float(len([cell for cell in localCells if cell.helper])) / float(numCells)
        immDensity = float(len([cell for cell in localCells if cell.immune])) / float(numCells)
    

    # ATTACK
    if cell.helper:
        for n in localCells:
            if n.infected: utilDict["ATTACK"] += 1.9 # + number of infected cells
            elif not n.immune and not n.infected: utilDict["ATTACK"] += 1.1 # + number of healthy cells
            elif n.immune and not n.helper: utilDict["ATTACK"] += 0.1 # + effector immune cells
            elif n.helper: utilDict["ATTACK"] -= 0.6 # bad if surrounded by helper cells
    else:
        for n in localCells:
            if n.infected and util.isNeighbor(cell.x, cell.y, n.x, n.y): utilDict["ATTACK"] += 390.5
            # elif not n.immune and util.isNeighbor(cell.x, cell.y, n.x, n.y): utilDict["ATTACK"] -= 10.

    # MOVE
    if cell.helper:
        if density < 0.25: utilDict["MOVE"] += 1.5
        else: utilDict["MOVE"] += 2.5
    else:
        # if density < 0.3: utilDict["MOVE"] += 2.5
        # else: utilDict["MOVE"] += 0.5
        utilDict["MOVE"] = 10.5

    # PASS
    if cell.helper:
        if density > 0.75 and hlpDense > 0.65: utilDict["PASS"] += np.inf
        else: utilDict["PASS"] -= np.inf
    else:
        # if density > 0.25 and immDensity > 0.35 and len([cell for cell in localCells if cell.infected])==0: utilDict["PASS"] += np.inf
        # else: 
        utilDict["PASS"] = -np.inf


    return max(utilDict, key=utilDict.get), utilDict # return action with maximum utility

 

def SmartUtility(cell, localCells, localArea):

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
    if cell.helper and numCells > 0:
        if numCells>0: utilDict["ATTACK"] += (2.5* float(numInf) / float(numCells)) * density

    else:
        for i in localCells:
            if i.infected: utilDict["ATTACK"] += 1.5 * cell.attack_success
            elif i.immune: utilDict["ATTACK"] -= 0.5 * cell.attack_success
            else: utilDict["ATTACK"] -= 2.5 * cell.attack_success

    # MOVE
    if cell.helper and numCells > 0:
        utilDict["MOVE"] += (float(numImmune) / float(numCells))

    elif numCells > 0:

        utilDict["MOVE"] += (float(numHealthy) - float(numInf) / float(numCells))
    else: utilDict["MOVE"] += np.inf
    
    # "PASS"
    if cell.helper and numCells > 0:
        if numCells>0: utilDict["PASS"] += (float(numHealthy) / float(numCells)) * density
    
    else:
        utilDict["PASS"] += -np.inf
    
    return max(utilDict, key=utilDict.get), utilDict # return action with maximum utility