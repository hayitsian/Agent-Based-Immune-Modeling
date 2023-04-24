from scipy.stats import bernoulli

from copy import deepcopy

class BaseCell():

    def __init__(self, x, y, repro=.1, die=.05, infected=False):
        self.repro_prob = repro #probability of Cell reproducing
        self.die_prob = die #probability of Cell dying
        self.x = x #x position in grid
        self.y = y #y position in grid
        self.infected = infected
        self.immune = False
    
    def reproduce(self, newX, newY):
        #reproduces cell if random number is less than reproduction probability

        newCell = deepcopy(self)
        newCell.x = newX
        newCell.y = newY

        return newCell
    

    def __str__(self):
        if self.infected: return "x"
        return "o"
    

class ImmuneCell(BaseCell):

    def __init__(self, x, y, util, attack_success, repro=.1, die=.05, infected=False):
        super().__init__(x, y, repro, die, infected)
        self.immune = True
        self.util = util #utility of cell. Should be a function that takes in an action, a ImmuneCell, and a Grid
        self.attack_success = attack_success #probability of attacking neighbor cells successfully
    
    def __str__(self):
        return "i"



def NaiveUtility(action, cell, grid):
    neighbors = grid.getNeighbors(cell.x, cell.y)
    utility = 0
    if action == "ATTACK":
        for n in neighbors:
            if n.infected: utility += 1 * cell.attack_success
            else: utility -= 1 * cell.attack_success
    else:
        for n in neighbors:
            if n.infected: utility -= 1
            else: utility += 1
    return utility