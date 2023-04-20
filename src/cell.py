from scipy.stats import bernoulli

class BaseCell():

    def __init__(self, x, y, repro=.1, die=.05, infected=False):
        self.repro_prob = repro #probability of Cell reproducing
        self.die_prob = die #probability of Cell dying
        self.x = x #x position in grid
        self.y = y #y position in grid
        self.infected = infected
    
    def reproduce(self, grid):
        #reproduces cell if random number is less than reproduction probability
        sample = bernoulli.rvs(self.repro_prob)
        if sample == 1:
            newCoords = grid.getEmptyNeighbor(self.x, self.y)
            if newCoords:
                newCell = BaseCell(newCoords[0], newCoords[1], self.repro_prob, self.die_prob, self.infected)
                grid.add(newCoords[0], newCoords[1], newCell)

    def infect(self, infection_prob, grid):
        #infects neighbor cells if infected with probability of infection
        if self.infected:
            neighbors = grid.getNeighbors(self.x, self.y)
            for neighbor in neighbors:
                sample = bernoulli.rvs(infection_prob)
                if sample == 1:
                    grid.add(neighbor.x,neighbor.y,BaseCell(neighbor.x,neighbor.y,infected=True))
    
    def die(self, grid):
        #kills cell if random number is less than death probability
        sample = bernoulli.rvs(self.die_prob)
        if sample == 1:
            grid.add(self.x, self.y, None)
    

class Grid():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for x in range(width)] for y in range(height)]

    
    def add(self, x, y, cell):
        self.grid[x][y] = cell

    def get(self, x, y):
        return self.grid[x][y]
    
    def getEmptyNeighbor(self, x,y):
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
    
    def getNeighbors(self, x,y):
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