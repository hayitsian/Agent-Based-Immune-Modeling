
from scipy.stats import bernoulli
from cell import BaseCell
import numpy as np

class Grid():

    def __init__(self, width, height, infection_prob):
        self.width = width
        self.height = height
        self.grid = [[None for i in range(width)] for j in range(height)]
        self.infection_prob = infection_prob

    def add(self, x, y, cell):
        self.grid[x][y] = cell

    def get(self, x, y):
        return self.grid[x][y]
    
    def update(self):

        for cell in self.getAllCells():
            self.reproduceCell(cell)
            self.infectCell(cell)
            self.die(cell)
    
    def reproduceCell(self, cell):
        #reproduces cell if random number is less than reproduction probability
        sample = bernoulli.rvs(cell.repro_prob)
        if sample == 1:
            newCoords = self.getEmptyNeighbor(cell.x, cell.y)
            if newCoords:

                self.add(newCoords[0], newCoords[1], cell.reproduce(newCoords[0], newCoords[1]))

        return self

    def infectCell(self, cell):
        #infects neighbor cells if infected with probability of infection

        if cell.infected:
            neighbors = self.getNeighbors(cell.x, cell.y)
            for neighbor in neighbors:
                sample = bernoulli.rvs(self.infection_prob)
                if sample == 1:
                    self.add(neighbor.x,neighbor.y,BaseCell(neighbor.x,neighbor.y,infected=True))

        return self
    
    def die(self, cell):
        #kills cell if random number is less than death probability
        sample = bernoulli.rvs(cell.die_prob)
        if sample == 1:
            self.add(cell.x, cell.y, None)
            return None
        return self
    
    
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
        cells = []
        for row in self.grid:
            for cell in row:
                if cell != None:
                    cells.append(cell)
        return cells
    

    def __str__(self):
        out = [[str(self.grid[x][y])[0] for x in range(self.width)]
               for y in range(self.height)]
        out = [[s.replace("N", " ") for s in line ] for line in out]
        out.reverse()
        return '\n'.join([''.join(x) for x in out])