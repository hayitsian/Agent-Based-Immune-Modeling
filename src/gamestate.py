
from scipy.stats import bernoulli
from cell import BaseCell, ImmuneCell, HelperImmuneCell
from cellAgents import NaiveUtility, SmartUtility, HelperUtility
import numpy as np
import random as rand
from copy import deepcopy
from itertools import chain

class GameState():

    def __init__(self, width=100, height=100, localRadius=None, effectorUtility = NaiveUtility, helperUtility = HelperUtility):
        self.width = width
        self.height = height
        self.cells = []
        self.grid = [[None for i in range(width)] for j in range(height)]
        if localRadius is None: self.localRadius = self.width / 10
        else: self.localRadius = localRadius
        self.effectorUtility = effectorUtility
        self.helperUtility = helperUtility


    def start(self, infection_prob, repro_prob, die_prob, immune_constant=0.75, attack_success=.75, helper_boost=1.25, numCells=200, numInfected=20, numImmune=20, numHelper=10):
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
                ic = ImmuneCell(cell.x, cell.y, self.effectorUtility, attack_success, immune_constant, repro=repro_prob, die=die_prob)
                self.cells[i] = ic
                self.add(cell.x, cell.y, ic)
                immune += 1

        helper = 0
        while helper < numHelper:
            i = rand.randint(0, len(self.cells)-1)
            cell = self.cells[i]
            if cell != None and not cell.infected and not cell.immune and not cell.helper:
                hc = HelperImmuneCell(cell.x, cell.y, attack_success, helper_boost, immune_constant, repro=repro_prob, die=die_prob)
                self.cells[i] = hc
                self.add(cell.x, cell.y, hc)
                helper += 1

        numCellsList = len(self.cells)
        numCellsGrid = len(self.getAllCells())
        assert numCellsList == numCellsGrid, f"Cells List {numCellsList}, cells grid {numCellsGrid}"

        return self



    def step(self):

        _numActivated = 0
        _numMoved = 0
        _numInfected = 0
        _numReproduce = 0
        _numEffected = 0 # immune attack or helper boosts
        _numDied = 0
        
        for cell in self.cells:

            cell.decrementCounter()
            
            # resMove = self.moveCell(cell)
            # if res: print("Cell moved")
            
            resRepr = self.reproduceCell(cell)
            _numReproduce += resRepr
            # if res: print("Cell reproduced")
            
            resInf = self.infectCell(cell)
            _numInfected += resInf
            # if res: print(f"Cells infected: {res}")
            
            resImm = self.immuneAct(cell)
            if resImm>0: 
                _numActivated += 1
                _numEffected += resImm
            elif resImm<0: _numMoved += 1
            # if res: print("Cell activated")

            resDie = self.die(cell)
            _numDied += resDie
            # if res: print("Cell died")


            numCellsList = len(self.cells)
            numCellsGrid = len(self.getAllCells())
            assert numCellsList == numCellsGrid, f"Cells List {numCellsList}, cells grid {numCellsGrid}, reproduce? {resRepr}, infected? {resInf}, activated? {resImm}, died? {resDie}"
            
        # self.updateGrid() # unnecessary
        numCells = len(self.cells)
        numInfected = sum([cell.infected for cell in self.cells])
        numImmune = sum([cell.immune for cell in self.cells])
        numHelper = sum([cell.helper for cell in self.cells])
        return numCells, numInfected, numImmune, numHelper, _numReproduce, _numMoved, _numInfected, _numDied, _numActivated, _numEffected


    def updateGrid(self):
        self.grid = [[None for i in range(self.width)] for j in range(self.height)]
        for cell in self.cells: self.add(cell.x, cell.y, cell)


    def add(self, x, y, cell):
        if cell in self.getAllCells():
            return
        self.grid[x][y] = cell


    def get(self, x, y):
        return self.grid[x][y]
    

    def moveCell(self, cell):
        if cell.immune:
            oldX = deepcopy(cell.x)
            oldY = deepcopy(cell.y)
            result = cell.move(self.getNeighbors(oldX, oldY),
                      self.width, self.height)
            if result:
                # update the grid
                self.add(oldX, oldY, None)
                self.add(cell.x, cell.y, cell)
            return -result
        return 0
    
    def immuneAct(self, cell):
        if cell.immune:
            if cell.activated: cell.activated = False
            attackUtil = cell.util("ATTACK",cell,self)
            passUtil = cell.util("PASS",cell,self)
            moveUtil, pos = cell.util("MOVE",cell,self)
            if attackUtil > passUtil and attackUtil > moveUtil:
                cell.activated = True
                if cell.helper: return self.immuneSupport(cell)
                return self.immuneAttack(cell)
            elif moveUtil > passUtil and moveUtil > attackUtil:
                if moveUtil == 0 or pos is None: return self.moveCell(cell) # random walk
                self.add(cell.x, cell.y, None)
                cell.moveTo(pos[0], pos[1])
                self.add(cell.x, cell.y, cell)
                return -1
            else: 
                if cell.helper: return self.immuneSuppression(cell)
                return 0
        return 0
    
    def immuneSupport(self, cell:HelperImmuneCell):
        # boosts immune cell proliferation and reduces infected
        # cell's infection probability
        localCells = self.getLocalCells(cell.x, cell.y)
        if len(localCells): return 0
        for _cell in localCells:
            if _cell.infected: _cell.boost(1./cell.helper_boost)
            elif _cell.immune: _cell.boost(cell.helper_boost)
        return 1

    def immuneSuppression(self, cell:HelperImmuneCell):
        # boosts healthy cell proliferation
        localCells = self.getLocalCells(cell.x, cell.y)
        if len(localCells): return 0
        for _cell in localCells:
            if not _cell.infected and not _cell.immune: _cell.boost(cell.helper_boost)
        return 1

    def immuneAttack(self, cell):
        neighbors = self.getNeighbors(cell.x, cell.y)
        if bernoulli.rvs(cell.attack_success) == 1:
            score = 0
            for neighbor in neighbors:
                self.add(neighbor.x,neighbor.y,None)
                self.cells.remove(neighbor) # NOTE: this could be an issue
                score += 1
            return score
        return 0

    def reproduceCell(self, cell):
        #reproduces cell if random number is less than reproduction probability
        sample = bernoulli.rvs(cell.repro_prob)
        if sample == 1:
            neighs = self.getEmptyNeighbors(cell.x, cell.y)
            if len(neighs) > 0:
                newCoords = rand.choice(neighs) # TODO this is not random
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
                    
                    if not neighbor.infected:
                        if neighbor in self.cells: self.cells.remove(neighbor)
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
    
    def getLocalCells(self, x, y): # NOTE keep in mind this radius

        lowerX = x-self.localRadius
        if lowerX < 0: lowerX = 0

        higherX = x+self.localRadius
        if higherX >= self.width: higherX = self.width - 1

        lowerY = y-self.localRadius
        if lowerY < 0: lowerY = 0

        higherY = y+self.localRadius
        if higherY >= self.height: higherY = self.height - 1

        lowerX = int(lowerX)
        lowerY = int(lowerY)
        higherX = int(higherX)
        higherY = int(higherY)


        subGrid = self.grid[lowerX:higherX][lowerY:higherY]
        return [cell for cell in list(chain(*subGrid)) if cell is not None]

    def getEmptyNeighbors(self, x, y):
        neighbors = []
        if y+1 < self.height and self.grid[x][y+1] is None:
            neighbors.append((x, y+1))
        if y-1 >= 0 and self.grid[x][y-1] is None:
            neighbors.append((x, y-1))
        if x-1 >= 0 and self.grid[x-1][y] is None:
            neighbors.append((x-1, y))
        if x+1 < self.width and self.grid[x+1][y] is None:
            neighbors.append((x+1, y))
        return neighbors

    def getNeighbors(self, x, y, includeEmpty=0):
        #returns list of neighbor Cell objects
        neighbors = []
        if y+1 < self.height:
            neighbors.append(self.grid[x][y+1])
        if y-1 >= 0:
            neighbors.append(self.grid[x][y-1])
        if x+1 < self.width:
            neighbors.append(self.grid[x+1][y])
        if x-1 >= 0:
            neighbors.append(self.grid[x-1][y])
        if not includeEmpty: return [neigh for neigh in neighbors if neigh is not None]
        return neighbors
    

    def getAllCells(self):
        #returns list of all Cell objects in grid
        return [cell for cell in list(chain(*self.grid)) if cell is not None]
    

    def __str__(self):
        out = [[str(self.grid[x][y])[0] for x in range(self.width)]
               for y in range(self.height)]
        out = [[s.replace("N", " ") for s in line ] for line in out]
        out.reverse()
        return '\n'.join([''.join(x) for x in out])