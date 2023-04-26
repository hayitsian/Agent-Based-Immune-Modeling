from scipy.stats import bernoulli

from copy import deepcopy
import random as rand
import util
import numpy as np

class BaseCell():

    def __init__(self, x, y, window, repro=.1, die=.05, infec=0.05, infected=False, helped=False):
        self.repro_prob = repro #probability of Cell reproducing
        self.die_prob = die #probability of Cell dying
        self.infection_prob = infec#probability of cell being infected
        self.x = x #x position in grid
        self.y = y #y position in grid
        self.window = window
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
            self.die_prob *= self._boost
            self.infection_prob *= self._boost
            self.boosted = False
            self._boost = 0.0

    def boost(self, boost:float, count:int):
        if self.boosted: self.revert() # new boosts override current

        if boost > 0. and count > 0 and not self.boosted:
            self.counter = count 
            self._boost = boost
            self.boosted = True
            self.repro_prob *= boost
            self.die_prob /= boost
            self.infection_prob /= boost
            if self.repro_prob > 1.0: self.repro_prob=1.0

    def reproduce(self, newX, newY):
        #reproduces cell if random number is less than reproduction probability

        newCell = deepcopy(self)
        newCell.x = newX
        newCell.y = newY

        return newCell

    def move(self, neighbors, width, height):
        # does not move, just for consistency
        return self.x, self.y

    def updateParams(self, localCells, localArea):
        density = float(len(localCells)) / float(localArea)

        if density > 0.85: self.boost(0.5, 10)

    def __str__(self):
        if self.infected: return "x"
        return "o"


class NaiveImmuneCell(BaseCell):

    def __init__(self, x, y, window, attack_success, immune_constant=0.75, repro=.1, die=.05):
        super().__init__(x, y, window, repro=repro*immune_constant, die=die, infec=0.0)
        self.immune = True
        self.attack_success = attack_success #probability of attacking neighbor cells successfully
        self.immuned_constant = immune_constant
        self.activated = False
        self.helper = False


    def _movementConditions(self, newX, newY, width, height, obsPoints):
        return width > newX >= 0 and height > newY >= 0 and (newX, newY) not in obsPoints


    def move(self, neighbors, width, height):
        # random walk movement
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
        elif randPoint==1 and self._movementConditions(self.x + 1, self.y, width, height, restrictedList):
            self.x = self.x + 1
        elif randPoint==2 and self._movementConditions(self.x, self.y - 1, width, height, restrictedList):
            self.y = self.y - 1
        elif randPoint==3 and self._movementConditions(self.x, self.y + 1, width, height, restrictedList):
            self.y = self.y + 1

        return self.x, self.y


    def updateParams(self, localCells, localArea):
        density = float(len(localCells)) / float(localArea)
        if len(localCells) > 0:
            immDensity = float(len([cell for cell in localCells if cell.immune])) / float(len(localCells))
            infDensity = float(len([cell for cell in localCells if cell.infected])) / float(len(localCells))
            hlpDensity = float(len([cell for cell in localCells if cell.immune and cell.helper])) / float(len(localCells))
            # harsher conditions then base, but worse penalty
            if immDensity > 0.65 and density > 0.5 and infDensity < 0.25: self.boost(0.3, 20)
            elif infDensity > 0.25 and hlpDensity > 0.2: self.boost(1.3, 5)

    def __str__(self):
        return "i"



class SmartImmuneCell(NaiveImmuneCell):

    def __init__(self, x, y, window, attack_success, immune_constant=0.75, repro=.1, die=.05):
        super().__init__(x, y, window, attack_success, immune_constant=immune_constant, repro=repro, die=die, infected=False)


    def move(self, neighbors, width, height):
        distDict = {}

        closeInfected = [cell for cell in neighbors if cell.infected]
        if len(closeInfected) == 0: return super().move(neighbors, width, height) # random walk if no infected
        for n in closeInfected:
            neighs = util.getNeighboringPositions(self.x, self.y, width, height)

            for newX, newY in neighs: distDict[(newX, newY)] = np.inf
            for newX, newY in neighs:
                dist = util.manhattanDistance((newX, newY), (n.x, n.y))
                if dist < distDict[(newX, newY)]: distDict[(newX, newY)] = dist

        if min(distDict.values()) == 0.0: return self.x, self.y
        return min(distDict, key=distDict.get)



class HelperImmuneCell(NaiveImmuneCell):

    def __init__(self, x, y, window, helper_boost=1.25, boost_count=5, immune_constant=1.0, repro=.1, die=.05):
        super().__init__(x, y, window, attack_success=0.0, immune_constant=immune_constant, repro=repro, die=die)
        self.helper_boost = helper_boost
        self.boost_count = boost_count
        self.activated = False
        self.helper = True
        self.suppress = False
        self.support = False

    def __str__(self):
        return "h"

    def updateParams(self, localCells, localArea):
        density = float(len(localCells)) / float(localArea)
        if len(localCells) > 0:
            hthlyDensity = float(len([cell for cell in localCells if cell.immune])) / float(len(localCells))
            infDensity = float(len([cell for cell in localCells if cell.infected])) / float(len(localCells))
            # harsher conditions then base, but worse penalty
            if infDensity > 0.55 and density > 0.5: self.boost(1.1, 10)
            elif density > 0.5 and hthlyDensity > 0.55: self.boost(0.9, 10)

    def move(self, neighbors, width, height):
        distDict = {}

        closeInfected = [cell for cell in neighbors if cell.immune]
        if len(closeInfected) == 0: return super().move(neighbors, width, height) # random walk if no immune
        for n in closeInfected:
            neighs = util.getNeighboringPositions(self.x, self.y, width, height)

            for newX, newY in neighs: distDict[(newX, newY)] = np.inf
            for newX, newY in neighs:
                dist = util.manhattanDistance((newX, newY), (n.x, n.y))
                if dist < distDict[(newX, newY)]: distDict[(newX, newY)] = dist

        if min(distDict.values()) == 0.0: return self.x, self.y
        return min(distDict, key=distDict.get)
