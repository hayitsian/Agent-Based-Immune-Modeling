#!/usr/bin/env python3
from cell import BaseCell, Grid
import random as rand

def start(infection_prob, repro_prob, die_prob,steps=100, width=100, height=100, numCells=200, numInfected=20):
    #creates grid and adds cells randomly to grid and randomly infects some of them
    grid = Grid(width, height)
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
    print("Initial Conditions:" + "\n" + "Number of living Cells: " + str(numCells) + "\n" + "Number of infected Cells: " + str(numInfected))
    print("Grid size: " + str(width) + "x" + str(height) + "\n")
    step = 1
    while step <= steps:
        cells = grid.getAllCells()
        print("Epoch: " + str(step))
        print("Number of living Cells: " + str(len(cells)))
        print("Number of infected Cells: " + str(len([cell for cell in cells if cell.infected])))
        
        for cell in cells:
            cell.reproduce(grid)
            cell.infect(infection_prob, grid)
            cell.die(grid)
        step += 1
    
def main():
    start(0.2, .5, .2)
    
main()