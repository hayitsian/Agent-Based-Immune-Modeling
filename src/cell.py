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

        return self

    def infect(self, infection_prob, grid):
        #infects neighbor cells if infected with probability of infection
        daughters = []
        if self.infected:
            neighbors = grid.getNeighbors(self.x, self.y)
            for neighbor in neighbors:
                sample = bernoulli.rvs(infection_prob)
                if sample == 1:
                    grid.add(neighbor.x,neighbor.y,BaseCell(neighbor.x,neighbor.y,infected=True))

        return self, daughters
    
    def die(self, grid):
        #kills cell if random number is less than death probability
        sample = bernoulli.rvs(self.die_prob)
        if sample == 1:
            grid.add(self.x, self.y, None)
            return None
        return self
    

    def __str__(self):

        pass