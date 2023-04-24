#!/usr/bin/env python3
from cell import BaseCell, ImmuneCell, NaiveUtility
from grid import Grid
import random as rand

import matplotlib.pyplot as plt


def start(infection_prob, repro_prob, die_prob, utility=NaiveUtility, attack_success=.75, width=100, height=100, numCells=200, numInfected=20, numImmune=20, verbose=False):
    #creates grid and adds cells randomly to grid and randomly infects some of them
    grid = Grid(width, height, infection_prob=infection_prob)
    print(str(grid))
    for i in range(numCells):
        x = rand.randint(0, width-1)
        y = rand.randint(0, height-1)
        if grid.get(x,y) == None:
            cell = BaseCell(x, y, repro_prob, die_prob, False)
            grid.add(x, y, cell)
        else:
            i -= 1
    infected = 0
    while infected < numInfected:
        x = rand.randint(0, width-1)
        y = rand.randint(0, height-1)
        cell = grid.get(x,y)
        if cell != None and not cell.infected:
            cell.infected = True
            infected += 1
    immune = 0
    while immune < numImmune:
        x = rand.randint(0, width-1)
        y = rand.randint(0, height-1)
        cell = grid.get(x,y)
        if cell != None and not cell.infected and not cell.immune:
            grid.add(cell.x, cell.y, ImmuneCell(cell.x, cell.y, utility, attack_success, repro=repro_prob, die=die_prob))
            immune += 1

    if verbose: print("Initial Conditions:" + "\n" + "Number of living Cells: " + str(numCells) + "\n" + "Number of infected Cells: " + str(numInfected) + "\n" + "Number of immune Cells: " + str(numImmune) + "\n")
    if verbose: print("Grid size: " + str(width) + "x" + str(height) + "\n")

    return grid


def step(grid, verbose=False):
    numCells, numInfected, numImmune, numActivated = grid.update(verbose)
    return numCells, numInfected, numImmune, numActivated

def main():
    INFECT_PROB = 0.05
    REPRODUCE_PROB = 0.09
    DEATH_PROB = 0.06
    ATTACK_SUCCESS = 0.75
    INIT_HEALTHY = 200
    INIT_INFECTED = 20
    INIT_IMMUNE = 20
    WIDTH = 100
    HEIGHT = 100
    EPOCHS = 500
    VERBOSE = True

    grid = start(INFECT_PROB, REPRODUCE_PROB, DEATH_PROB, width=WIDTH, height=HEIGHT, attack_success=ATTACK_SUCCESS, numCells=INIT_HEALTHY, numInfected=INIT_INFECTED, numImmune=INIT_IMMUNE, verbose=VERBOSE)

    numSteps = 0

    cellCount = []
    infCellCount = []
    immCellCount = []
    accImmCellCount = []

    cellCount.append(INIT_HEALTHY)
    infCellCount.append(INIT_INFECTED)
    immCellCount.append(INIT_IMMUNE)
    accImmCellCount.append(0)

    while numSteps < EPOCHS:

        numCells, numInfected, numImmune, numActivated = step(grid, VERBOSE)

        if VERBOSE: print("Epoch: " + str(numSteps) + "\n", end='\r')
        if VERBOSE: print(f"Number of Cells: {numCells}")
        if VERBOSE: print(f"Number of Infected Cells: {numInfected}")
        if VERBOSE: print(f"Number of Immune Cells: {numImmune}")
        if VERBOSE: print(f"Number of Activated Immune Cells: {numActivated}")
        if VERBOSE: print(str(grid) + "\n", end='\r')

        cellCount.append(numCells)
        infCellCount.append(numInfected)
        immCellCount.append(numImmune)
        accImmCellCount.append(numActivated)

        numSteps += 1

    FIGURE_TITLE = f"Cell counts over {EPOCHS} steps {WIDTH}x{HEIGHT} grid\nInfectProb: {INFECT_PROB} ReproProb: {REPRODUCE_PROB}\nDeathProb: {DEATH_PROB} AttackSuccess: {ATTACK_SUCCESS}"
    FIGURE_NAME = FIGURE_TITLE.replace("\n", " ") + ".png"

    plt.plot(list(range(EPOCHS+1)), cellCount, label="Total cell count")
    plt.plot(list(range(EPOCHS+1)), infCellCount, label="Infected cell count")
    plt.plot(list(range(EPOCHS+1)), immCellCount, label="Immune cell count")
    plt.plot(list(range(EPOCHS+1)), accImmCellCount, label="Activated Immune cell count")
    plt.title(FIGURE_TITLE)
    plt.xlabel("Steps")
    plt.ylabel("Cell count")
    plt.legend()
    plt.savefig(FIGURE_NAME)

main()