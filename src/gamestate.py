
from scipy.stats import bernoulli
from cell import BaseCell, ImmuneCell, NaiveUtility
import numpy as np
import random as rand
from copy import deepcopy

class GameState():

    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.cells = []
        self.grid = [[None for i in range(width)] for j in range(height)]


    def start(self, infection_prob, repro_prob, die_prob, attack_success=.75, utility=NaiveUtility, numCells=200, numInfected=20, numImmune=20):
        #creates grid and adds cells randomly to grid and randomly infects some of them
        self.infection_prob = infection_prob
        self.repro_prob = repro_prob
        self.die_prob = die_prob

        for i in range(numCells):
            x = rand.randint(0, self.width-1)
            y = rand.randint(0, self.height-1)
            if self.get(x,y) == None:
                cell = BaseCell(x, y, repro_prob, die_prob, False)
                self.add(x, y, cell)
                self.cells.append(cell)
            else:
                i -= 1

        numCellsList = len(self.cells)
        numCellsGrid = len(self.getAllCells())
        assert numCellsList == numCellsGrid, f"Cells List {numCellsList}, cells grid {numCellsGrid}"

        infected = 0
        while infected < numInfected:
            i = rand.randint(0, len(self.cells)-1)
            cell = self.cells[i]
            if cell != None and not cell.infected:
                cell.infected = True
                infected += 1
        immune = 0
        while immune < numImmune:
            i = rand.randint(0, len(self.cells)-1)
            cell = self.cells[i]
            if cell != None and not cell.infected and not cell.immune:
                ic = ImmuneCell(cell.x, cell.y, utility, attack_success, repro=repro_prob, die=die_prob)
                self.cells[i] = ic
                self.add(cell.x, cell.y, ic)
                immune += 1

        numCellsList = len(self.cells)
        numCellsGrid = len(self.getAllCells())
        assert numCellsList == numCellsGrid, f"Cells List {numCellsList}, cells grid {numCellsGrid}"

        return self


    def step(self):

        numActivated = 0

        for cell in self.cells:
            
            res = self.moveCell(cell)
            if res: print("Cell moved")
            
            res = self.reproduceCell(cell)
            if res: print("Cell reproduced")
            
            res = self.infectCell(cell)
            if res: print(f"Cells infected: {res}")
            
            res = self.immuneAct(cell)
            numActivated += res
            if res: print("Cell activated")

            res = self.die(cell)
            if res: print("Cell died")

            numCellsList = len(self.cells)
            numCellsGrid = len(self.getAllCells())
            assert numCellsList == numCellsGrid, f"Cells List {numCellsList}, cells grid {numCellsGrid}"
            
        # self.updateGrid()

        # TODO these metrics are wrong
        numCells = len(self.cells)
        numInfected = sum([cell.infected for cell in self.cells])
        numImmune = sum([cell.immune for cell in self.cells])
        return numCells, numInfected, numImmune, numActivated


    def updateGrid(self):
        self.grid = [[None for i in range(self.width)] for j in range(self.height)]
        for cell in self.cells: self.add(cell.x, cell.y, cell)


    def add(self, x, y, cell):
        self.grid[x][y] = cell

    def get(self, x, y):
        return self.grid[x][y]
    
    def moveCell(self, cell):
        if cell.immune:
            oldX = deepcopy(cell.x)
            oldY = deepcopy(cell.y)
            result = cell.move(self.getNeighbors(cell.x, cell.y),
                      self.width, self.height)
            if result:
                # update the grid
                self.add(oldX, oldY, None)
                self.add(cell.x, cell.y, cell)
    
    def immuneAct(self, cell):
        if cell.immune:
            attackUtil = cell.util("ATTACK",cell,self)
            passUtil = cell.util("PASS",cell,self)
            if attackUtil > passUtil:
                return self.immuneAttack(cell)

            else: return 0
        return 0

    def immuneAttack(self, cell):
        neighbors = self.getNeighbors(cell.x, cell.y)
        if bernoulli.rvs(cell.attack_success) == 1:
            for neighbor in neighbors:
                self.add(neighbor.x,neighbor.y,None)
                if neighbor in self.cells: self.cells.remove(neighbor) # NOTE: this could be an issue
            return 1
        return 0

    def reproduceCell(self, cell):
        #reproduces cell if random number is less than reproduction probability
        sample = bernoulli.rvs(cell.repro_prob)
        if sample == 1:
            newCoords = self.getEmptyNeighbor(cell.x, cell.y) # TODO this is not random
            if newCoords:
                newCell = cell.reproduce(newCoords[0], newCoords[1])
                self.add(newCoords[0], newCoords[1], newCell)
                self.cells.append(newCell)
                return 1
        return 0

    def infectCell(self, cell):
        #infects neighbor cells if infected with probability of infection
        numInfected = 0
        if cell.infected:
            neighbors = self.getNeighbors(cell.x, cell.y)
            for neighbor in neighbors:
                if neighbor.immune: continue
                sample = bernoulli.rvs(self.infection_prob)
                if sample == 1:
                    if neighbor in self.cells: self.cells.remove(neighbor)
                    if not neighbor.infected:
                        neighbor.infected=True
                        self.cells.append(neighbor)
                        self.add(neighbor.x, neighbor.y, neighbor)
                        numInfected += 1
        return numInfected
    
    def die(self, cell):
        #kills cell if random number is less than death probability
        sample = bernoulli.rvs(cell.die_prob)
        if sample == 1:
            self.add(cell.x, cell.y, None)
            if cell in self.cells: self.cells.remove(cell) # NOTE: this could be an issue
            return 1
        return 0
    
    
    def getEmptyNeighbor(self, x, y):
        #checks neighbors for an empty space around x and y coordinates
        #returns coordinates of empty space or False if none are found
        #if x is at max width or y at max height, does not check outside of range
        if y+1 < self.height and self.grid[x][y+1] == None:
            return (x, y+1)
        elif y-1 >= 0 and self.grid[x][y-1] == None:
            return (x, y-1)
        elif x+1 < self.width and self.grid[x+1][y] == None:
            return (x+1, y)
        elif x-1 >= 0 and self.grid[x-1][y] == None:
            return (x-1, y)
        return False
    
    def getNeighbors(self, x, y):
        #returns list of neighbor Cell objects
        neighbors = []
        if y+1 < self.height and self.grid[x][y+1] != None:
            neighbors.append(self.grid[x][y+1])
        if y-1 >= 0 and self.grid[x][y-1] != None:
            neighbors.append(self.grid[x][y-1])
        if x+1 < self.width and self.grid[x+1][y] != None:
            neighbors.append(self.grid[x+1][y])
        if x-1 >= 0 and self.grid[x-1][y] != None:
            neighbors.append(self.grid[x-1][y])
        return neighbors
    
    def getAllCells(self):
        #returns list of all Cell objects in grid
        return [cell for cell in self.grid if cell is not None]
    

    def __str__(self):
        out = [[str(self.grid[x][y])[0] for x in range(self.width)]
               for y in range(self.height)]
        out = [[s.replace("N", " ") for s in line ] for line in out]
        out.reverse()
        return '\n'.join([''.join(x) for x in out])