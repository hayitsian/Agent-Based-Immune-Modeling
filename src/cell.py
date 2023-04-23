from scipy.stats import bernoulli

from copy import deepcopy

class BaseCell():

    def __init__(self, x, y, repro=.1, die=.05, infected=False):
        self.repro_prob = repro #probability of Cell reproducing
        self.die_prob = die #probability of Cell dying
        self.x = x #x position in grid
        self.y = y #y position in grid
        self.infected = infected
    
    def reproduce(self, newX, newY):
        #reproduces cell if random number is less than reproduction probability

        newCell = deepcopy(self)
        newCell.x = newX
        newCell.y = newY

        return newCell
    

    def __str__(self):
        if self.infected: return "i"
        return "o"
    

class ImmuneCell(BaseCell):

    pass