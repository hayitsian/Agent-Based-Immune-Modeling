#!/usr/bin/env python3

from gamestate import GameState
import random as rand
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer


def plot(EPOCHS, FIGURE_TITLE, FIGURE_NAME, _labels, data):
    for i in range(len(data)):
        plt.plot(list(range(EPOCHS+1)), data[i], label=_labels[i])

    plt.title(FIGURE_TITLE)
    plt.xlabel("Steps")
    plt.ylabel("# Cells")
    plt.legend()
    plt.savefig(FIGURE_NAME)
    plt.close()


def main(INFECT_PROB = 0.035,
    REPRODUCE_PROB = 0.05,
    DEATH_PROB = 0.03,
    ATTACK_SUCCESS = 0.85,
    IMMUNE_CONSTANT = 0.95,
    HELPER_BOOST = 1.2,
    BOOST_COUNT = 5,
    INIT_HEALTHY = 60,
    INIT_INFECTED = 10,
    INIT_IMMUNE = 10,
    INIT_HELPER = 10,
    WIDTH = 50,
    HEIGHT = 50,
    EPOCHS = 1500,
    PLOT = True,
    VERBOSE = True
    ):

    game = GameState(WIDTH, HEIGHT)

    game.start(INFECT_PROB, REPRODUCE_PROB, DEATH_PROB, 
                 attack_success=ATTACK_SUCCESS, numCells=INIT_HEALTHY, 
                 numInfected=INIT_INFECTED, numImmune=INIT_IMMUNE,
                 numHelper = INIT_HELPER, immune_constant=IMMUNE_CONSTANT,
                 helper_boost=HELPER_BOOST, boost_count=BOOST_COUNT)

    if VERBOSE: print("Initial Conditions:" + "\n" + "Number of living Cells: " + str(INIT_HEALTHY) + "\n" + "Number of infected Cells: " 
                      + str(INIT_INFECTED) + "\n" + "Number of immune Cells: " + str(INIT_IMMUNE) + "\n")
    if VERBOSE: print("Grid size: " + str(game.width) + "x" + str(game.height) + "\n")
    if VERBOSE: print(str(game) + "\n", end='\r')

    

    cellCount = []
    infCellCount = []
    immCellCount = []
    healthyCellCount = []
    helperCellCount = []
    effectorCellCount = []

    accImmCellCount = []
    reprCellCount = []
    moveCellCount = []
    infTurnCellCount = []
    dieCellCount = []
    killedCellCount = []
    boostedCellCount = []
    suppressedCellCount = []

    cellCount.append(INIT_HEALTHY)
    infCellCount.append(INIT_INFECTED)
    immCellCount.append(INIT_IMMUNE)
    helperCellCount.append(INIT_HELPER)
    healthyCellCount.append(INIT_HEALTHY - INIT_IMMUNE - INIT_INFECTED)
    effectorCellCount.append(INIT_IMMUNE - INIT_HELPER)

    accImmCellCount.append(0)
    reprCellCount.append(0)
    moveCellCount.append(0)
    infTurnCellCount.append(0)
    dieCellCount.append(0)
    killedCellCount.append(0)
    boostedCellCount.append(0)
    suppressedCellCount.append(0)

    startTime = default_timer()

    numSteps = 0

    while numSteps < EPOCHS:

        numSteps += 1

        numCells, numInfected, numImmune, numHelper, _numReproduce, _numMoved, _numInfectedTurn, _numDied, _numActivated, _numKilled, _numBoosted, _numSuppressed = game.step()
        numHealthy = numCells - numImmune - numInfected
        numEffector = numImmune - numHelper

        if VERBOSE: print("Epoch: " + str(numSteps) + "\n", end='\r')
        if VERBOSE: print(f"Number of Cells: {numCells}")
        if VERBOSE: print(f"Number of Healthy Cells: {numHealthy}")
        if VERBOSE: print(f"Number of Infected Cells: {numInfected}")
        if VERBOSE: print(f"Number of Immune Cells: {numImmune}")
        if VERBOSE: print(f"Number of Effector Cells: {numEffector}")
        if VERBOSE: print(f"Number of Helper Cells: {numHelper}")
        if VERBOSE: print(f"Number of Cells to Reproduce: {_numReproduce}")
        if VERBOSE: print(f"Number of Cells to Move: {_numMoved}")
        if VERBOSE: print(f"Number of Cells Infected this turn: {_numInfectedTurn}")
        if VERBOSE: print(f"Number of Cells who Died: {_numDied}")
        if VERBOSE: print(f"Number of Cells Activated: {_numActivated}")
        if VERBOSE: print(f"Number of Cells Killed: {_numKilled}")
        if VERBOSE: print(f"Number of Cells Boosted: {_numBoosted}")
        if VERBOSE: print(f"Number of Cells Suppressed: {_numSuppressed}")
        if VERBOSE: print(str(game) + "\n", end='\r')

        cellCount.append(numCells)
        infCellCount.append(numInfected)
        immCellCount.append(numImmune)
        healthyCellCount.append(numHealthy)
        helperCellCount.append(numHelper)
        effectorCellCount.append(numEffector)
    
        accImmCellCount.append(_numActivated)
        reprCellCount.append(_numReproduce)
        moveCellCount.append(_numMoved)
        infTurnCellCount.append(_numInfectedTurn)
        dieCellCount.append(_numDied)
        killedCellCount.append(_numKilled)
        boostedCellCount.append(_numBoosted)
        suppressedCellCount.append(_numSuppressed)

    time = default_timer() - startTime
    if VERBOSE: print(f"Simulation took: {time}")

    FIGURE_TITLE = f"Cell counts over {EPOCHS} steps {WIDTH}x{HEIGHT} grid\nInfectProb: {INFECT_PROB} ReproProb: {REPRODUCE_PROB} DeathProb: {DEATH_PROB} AttackSuccess: {ATTACK_SUCCESS}\nWith smartUtility immune cell movement"
    FIGURE_NAME = FIGURE_TITLE.replace("\n", " ") + ".png"
    labels = ["Total cell count", "Infected cell count", "Immune cell count", "Healthy cell count", "Helper cell count", "Effector cell count"]
    data = [cellCount, infCellCount, immCellCount, healthyCellCount, helperCellCount, effectorCellCount]

    if PLOT: plot(EPOCHS, FIGURE_TITLE, FIGURE_NAME, labels, data)

    FIGURE_TITLE = f"Cell actions over {EPOCHS} steps {WIDTH}x{HEIGHT} grid\nInfectProb: {INFECT_PROB} ReproProb: {REPRODUCE_PROB} DeathProb: {DEATH_PROB} AttackSuccess: {ATTACK_SUCCESS}\nWith smartUtility immune cell movement"
    FIGURE_NAME = FIGURE_TITLE.replace("\n", " ") + ".png"
    labels = ["Activated cell count", "Reproduced cell count", "Moved cell count", "Infected cell count", "Died cell count", "Killed cell count", "Boosted cell count", "Suppressed cell count"]
    data = [accImmCellCount, reprCellCount, moveCellCount, infTurnCellCount, dieCellCount, killedCellCount, boostedCellCount, suppressedCellCount]

    if PLOT: plot(EPOCHS, FIGURE_TITLE, FIGURE_NAME, labels, data)


    return [cellCount, infCellCount, immCellCount, healthyCellCount, helperCellCount, effectorCellCount, accImmCellCount, reprCellCount, moveCellCount, infTurnCellCount, dieCellCount, killedCellCount, boostedCellCount]

main()