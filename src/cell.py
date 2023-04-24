from scipy.stats import bernoulli

from copy import deepcopy
import random as rand

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
    
    def _movementConditions(self, newX, newY, width, height, obsPoints):
        return width > newX >= 0 and height > newY >= 0 and (newX, newY) not in obsPoints

    def move(self, neighbors, width, height):
        randPoint = rand.randint(0, 3)
        numNeighbors = len(neighbors)
        restrictedList = []
        # for each neighbor
        if numNeighbors > 0:
            for neigh in neighbors:
                restrictedList.append((neigh.x, neigh.y))
                # add its coords to some list

        if randPoint==0 and self._movementConditions(self.x - 1, self.y, width, height, restrictedList):
            self.x = self.x - 1
            return 1
        elif randPoint==1 and self._movementConditions(self.x + 1, self.y, width, height, restrictedList):
            self.x = self.x + 1
            return 1
        elif randPoint==2 and self._movementConditions(self.y - 1, self.y, width, height, restrictedList):
            self.y = self.y - 1
            return 1
        elif randPoint==3 and self._movementConditions(self.y + 1, self.y, width, height, restrictedList):
            self.y = self.y + 1
            return 1

        return 0

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