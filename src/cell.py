from scipy.stats import bernoulli

from copy import deepcopy
import random as rand
import util

class BaseCell():

    def __init__(self, x, y, repro=.1, die=.05, infected=False):
        self.repro_prob = repro #probability of Cell reproducing
        self.die_prob = die #probability of Cell dying
        self.x = x #x position in grid
        self.y = y #y position in grid
        self.infected = infected
        self.immune = False
        self.helped = False
    
    def reproduce(self, newX, newY):
        #reproduces cell if random number is less than reproduction probability

        newCell = deepcopy(self)
        newCell.x = newX
        newCell.y = newY

        return newCell
    
    def boostReproduction(self):
        if not self.helped:
            self.helped = True
            self.repro_prob *= 2

    def __str__(self):
        if self.infected: return "x"
        return "o"


class ImmuneCell(BaseCell):

    def __init__(self, x, y, util, attack_success, repro=.1, die=.05, infected=False):
        super().__init__(x, y, repro, die, infected)
        self.immune = True
        self.util = util #utility of cell. Should be a function that takes in an action, a ImmuneCell, and a Grid
        self.attack_success = attack_success #probability of attacking neighbor cells successfully
        self.activated = False
        self.helper = False
    
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

    def __init__(self, x, y, attack_success, repro=.1, die=.05, infected=False):
        super().__init__(x, y, self.HelperUtility, attack_success, repro, die, infected)
        self.helper = True

    def HelperUtility(self, action, grid):
        localCells = grid.getLocalCells(self.x, self.y)
        numCells = len(localCells)
        numImmune = len([cell for cell in localCells if cell.immune])
        numInf = len([cell for cell in localCells if cell.infected])
        numHealthy = numCells - numImmune - numInf

        MOVE_CONSTANT = 2.
        density = numCells / (grid.localRadius**2)

        utility = 0

        if action == "ATTACK":
            utility += (numCells - numHealthy) / float(numCells) * density

        elif action == "PASS":
            utility += (numHealthy) / float(numCells) * density

        elif action == "MOVE":
            densDict = {}
            emptyNeigh = grid.getEmptyNeighbors(self.x, self.y)
            if len(emptyNeigh) > 0:
                for newX, newY in emptyNeigh: densDict[(newX, newY)] = 0
                for newX, newY in emptyNeigh:
                    numLocalCells = len(grid.getLocalCells(newX, newY))
                    dens = numLocalCells / grid.localRadius**2
                    if dens > densDict[(newX, newY)]: densDict[(newX, newY)] = dens
            pos = max(densDict, key=densDict.get)
            diff = densDict[pos] - density
            return (diff * MOVE_CONSTANT, pos)

        # if surrounded by healthy cells
            # boost reproductive probability

        # if surrounded by infected cells
            # boost immune cell reproductive probability
            # reduce infected probability


    def __str__(self):
        return "h"

