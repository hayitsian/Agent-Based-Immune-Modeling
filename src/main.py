#!/usr/bin/env python3

from gamestate import GameState
import random as rand
import numpy as np
import matplotlib.pyplot as plt


def plot(EPOCHS, FIGURE_TITLE, FIGURE_NAME, cellCount, infCellCount, immCellCount, accImmCellCount):

    plt.plot(list(range(EPOCHS+1)), cellCount, label="Total cell count")
    plt.plot(list(range(EPOCHS+1)), infCellCount, label="Infected cell count")
    plt.plot(list(range(EPOCHS+1)), immCellCount, label="Immune cell count")
    # plt.plot(list(range(EPOCHS+1)), accImmCellCount, label="Activated Immune cell count")
    plt.title(FIGURE_TITLE)
    plt.xlabel("Steps")
    plt.ylabel("Cell count")
    plt.legend()
    plt.savefig(FIGURE_NAME)


def main():
    INFECT_PROB = 0.055
    REPRODUCE_PROB = 0.07
    DEATH_PROB = 0.06
    ATTACK_SUCCESS = 0.85
    INIT_HEALTHY = 30
    INIT_INFECTED = 5
    INIT_IMMUNE = 5
    WIDTH = 50
    HEIGHT = 50
    EPOCHS = 2500
    VERBOSE = True

    game = GameState(WIDTH, HEIGHT)

    game.start(INFECT_PROB, REPRODUCE_PROB, DEATH_PROB, 
                 attack_success=ATTACK_SUCCESS, numCells=INIT_HEALTHY, 
                 numInfected=INIT_INFECTED, numImmune=INIT_IMMUNE)

    if VERBOSE: print("Initial Conditions:" + "\n" + "Number of living Cells: " + str(INIT_HEALTHY) + "\n" + "Number of infected Cells: " 
                      + str(INIT_INFECTED) + "\n" + "Number of immune Cells: " + str(INIT_IMMUNE) + "\n")
    if VERBOSE: print("Grid size: " + str(game.width) + "x" + str(game.height) + "\n")
    if VERBOSE: print(str(game) + "\n", end='\r')

    numSteps = 0

    cellCount = []
    infCellCount = []
    immCellCount = []
    accImmCellCount = []
    healthyCellCount = []

    cellCount.append(INIT_HEALTHY)
    infCellCount.append(INIT_INFECTED)
    immCellCount.append(INIT_IMMUNE)
    accImmCellCount.append(0)
    healthyCellCount.append(INIT_HEALTHY - INIT_IMMUNE - INIT_INFECTED)

    while numSteps < EPOCHS:

        numCells, numInfected, numImmune, numActivated = game.step()
        numHealthy = numCells - numImmune - numInfected

        if VERBOSE or True: print("Epoch: " + str(numSteps) + "\n", end='\r')
        if VERBOSE: print(f"Number of Cells: {numCells}")
        if VERBOSE: print(f"Number of Infected Cells: {numInfected}")
        if VERBOSE: print(f"Number of Immune Cells: {numImmune}")
        if VERBOSE: print(f"Number of Healthy Cells: {numHealthy}")
        if VERBOSE: print(str(game) + "\n", end='\r')

        cellCount.append(numCells)
        infCellCount.append(numInfected)
        immCellCount.append(numImmune)
        accImmCellCount.append(numActivated)
        healthyCellCount.append(numHealthy)

        numSteps += 1

    FIGURE_TITLE = f"Cell counts over {EPOCHS} steps {WIDTH}x{HEIGHT} grid\nInfectProb: {INFECT_PROB} ReproProb: {REPRODUCE_PROB} DeathProb: {DEATH_PROB} AttackSuccess: {ATTACK_SUCCESS}\nWith smartwalk & smartactivation immune cell movement"
    FIGURE_NAME = FIGURE_TITLE.replace("\n", " ") + ".png"

    if VERBOSE: plot(EPOCHS, FIGURE_TITLE, FIGURE_NAME, cellCount, infCellCount, immCellCount, accImmCellCount)

    return [cellCount, infCellCount, immCellCount, accImmCellCount]

main()