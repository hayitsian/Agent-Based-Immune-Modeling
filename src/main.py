#!/usr/bin/env python3
from cell import BaseCell, ImmuneCell, NaiveUtility
from grid import Grid
import random as rand



def start(infection_prob, repro_prob, die_prob, utility=NaiveUtility, attack_success=.75, width=100, height=100, numCells=200, numInfected=20,numImmune=20, verbose=False):
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
            grid.add(cell.x, cell.y, ImmuneCell(cell.x, cell.y, utility, attack_success))
            immune += 1

    if verbose: print("Initial Conditions:" + "\n" + "Number of living Cells: " + str(numCells) + "\n" + "Number of infected Cells: " + str(numInfected) + "\n" + "Number of immune Cells: " + str(numImmune) + "\n")
    if verbose: print("Grid size: " + str(width) + "x" + str(height) + "\n")

    return grid


def step(grid, infection_prob, verbose=False):

    # cells = grid.getAllCells()

    grid.update()


    if verbose: print("Number of living Cells: " + str(len(grid.getAllCells())))
    if verbose: print("Number of infected Cells: " + str(len([cell for cell in grid.getAllCells() if cell.infected])))
    if verbose: print("Number of immune Cells: " + str(len([cell for cell in grid.getAllCells() if cell.immune])))
    

        
    


def main():
    INFECT_PROB = 0.2
    REPRODUCE_PROB = 0.5
    DEATH_PROB = 0.2
    EPOCHS = 100
    VERBOSE = True

    grid = start(INFECT_PROB, REPRODUCE_PROB, DEATH_PROB, verbose=VERBOSE)

    numSteps = 0

    while numSteps < EPOCHS:

        if VERBOSE: print("Epoch: " + str(numSteps))
        step(grid, INFECT_PROB, VERBOSE)

        #if VERBOSE: print(str(grid))

        numSteps += 1

main()