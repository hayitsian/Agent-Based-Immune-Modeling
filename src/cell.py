from scipy.stats import bernoulli

from copy import deepcopy
import random as rand
import util
from cellAgents import NaiveUtility, HelperUtility

class BaseCell():

    def __init__(self, x, y, repro=.1, die=.05, infected=False, helped=False):
        self.repro_prob = repro #probability of Cell reproducing
        self.die_prob = die #probability of Cell dying
        self.x = x #x position in grid
        self.y = y #y position in grid
        self.infected = infected
        self.helped = helped
        self.counter = 0 # counter for boosts
        self._boost = 0.0
        # identifiers
        self.immune = False
        self.helper = False
        self.boosted = False
    
    def decrementCounter(self):
        if self.counter == 1:
            self.revert()
        
        if self.counter > 0: 
            self.counter -= 1
        
    def revert(self):
        if self._boost > 0.:
            self.repro_prob /= self._boost
            self.boosted = False
            self._boost = 0.0

    def boost(self, boost:float, count:int):
        if boost > 0. and count > 0 and not self.boosted:
            self.counter = count 
            self._boost = boost
            self.boosted = True
            self.repro_prob *= boost
            if self.repro_prob > 1.0: self.repro_prob=1.0

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

    def __init__(self, x, y, util, attack_success, immune_constant=0.75, repro=.1, die=.05, infected=False):
        super().__init__(x, y, repro*immune_constant, die, infected)
        self.immune = True
        self.util = util #utility of cell. Should be a function that takes in an action, a ImmuneCell, and a Grid
        self.attack_success = attack_success #probability of attacking neighbor cells successfully
        self.immuned_constant = immune_constant
        self.activated = False
        self.helper = False

    def revert(self):
        if self._boost > 0.:
            self.repro_prob /= 2*self._boost
            self.boosted = False
            self._boost = 0.0


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
        elif randPoint==2 and self._movementConditions(self.x, self.y - 1, width, height, restrictedList):
            self.y = self.y - 1
            return 1
        elif randPoint==3 and self._movementConditions(self.x, self.y + 1, width, height, restrictedList):
            self.y = self.y + 1
            return 1

        return 0

    def moveTo(self, x, y):
        self.x = x
        self.y = y
        return self

    def __str__(self):
        return "i"


class HelperImmuneCell(ImmuneCell):

    def __init__(self, x, y, attack_success, helper_boost=1.25, boost_count=5, immune_constant=1.0, repro=.1, die=.05, infected=False):
        super().__init__(x, y, HelperUtility, attack_success, immune_constant, repro, die, infected)
        self.helper_boost = helper_boost
        self.boost_count = boost_count
        self.activated = False
        self.helper = True
        self.suppress = False
        self.support = False

    def __str__(self):
        return "h"

