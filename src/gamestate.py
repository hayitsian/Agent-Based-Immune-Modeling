
from scipy.stats import bernoulli
from cell import BaseCell, NaiveImmuneCell, SmartImmuneCell, HelperImmuneCell
from cellAgents import NaiveUtility, SmartUtility
import numpy as np
import random as rand
from copy import deepcopy
from itertools import chain

class GameState():

    def __init__(self, width=100, height=100,
                 utility = NaiveUtility, autocrineWindow = 2,
                 paracrineWindow = 4, endocrineWindow = 8):
        
        self.width = width
        self.height = height
        self.cells = []
        self.grid = [[None for i in range(width)] for j in range(height)]


        self.utility = utility

        self.autocrineWindow = autocrineWindow
        self.paracrineWindow = paracrineWindow
        self.endocrineWindow = endocrineWindow



    def load(self, cells: list[BaseCell]):
        # loads in a gamestate as a list of cells
        # the cells' x,y position must be within this gamestate's grid width & height

        for _cell in cells:
            assert _cell.x >= 0 and _cell.x < self.width, f"Cell x-pos {_cell.x} greater than gameState width {self.width}"
            assert _cell.y >= 0 and _cell.y < self.height, f"Cell y-pos {_cell.y} greater than gameState height {self.height}"
            for __cell in self.cells: assert _cell.x != __cell.x or _cell.y != __cell.y, f"Cell at {_cell.x}, {_cell.y} already exists"
            self.cells.append(_cell)

        
        self.cells = cells
        self.updateGrid()

        return self
    


    def updateGrid(self):
        self.grid = [[None for i in range(self.width)] for j in range(self.height)]
        for cell in self.cells: self.add(cell.x, cell.y, cell)


    def add(self, x, y, cell):
        if cell in self.getAllCellsGrid():
            return
        self.grid[x][y] = cell


    def get(self, x, y):
        return self.grid[x][y]
    

    
    def immuneAct(self, cell:NaiveImmuneCell, action:str):
        if cell.immune:
            if cell.helper: cell.suppress = cell.support = False
            if cell.activated: cell.activated = False

            lowerX, lowerY, higherX, higherY = self.getLocalArea(cell.x, cell.y, cell.window)
            localArea = (higherX - lowerX) * (higherY - lowerY)

            if action == "ATTACK": # attack
                cell.activated = True
                if cell.helper: 
                    cell.activate(self.getLocalCells(cell.x, cell.y, cell.window), localArea)
                    if cell.suppress: return self.immuneSuppression(cell)
                    elif cell.support: return self.immuneSupport(cell)
                return self.immuneAttack(cell)
            
            elif action == "MOVE": # move
                return self.moveCell(cell)
            
            elif action == "PASS": # pass/suppress
                cell.die_prob = 0.5
                res = self.die(cell)
                if not res: cell.die_prob = 0.01
                return res
        return 0
    


    def moveCell(self, cell):
        if cell.immune:
            localCells = self.getLocalCells(cell.x, cell.y, self.endocrineWindow) # movement direction gets full endocrine signal
            oldX = deepcopy(cell.x)
            oldY = deepcopy(cell.y)
            newx, newy = cell.move(localCells,
                      self.width, self.height)
            
            if oldX != newx or oldY != newy:
                if self.grid[newx][newy] is not None and self.grid[oldX][oldY] is not None:
                    oldCel = self.grid[newx][newy]
                    oldCel.x = oldX
                    oldCel.y = oldY
                    self.grid[oldX][oldY] = oldCel
                    self.grid[newx][newy] = cell
                    return -2 # swap
                if self.grid[oldX][oldY] is None:
                    return 0
                self.grid[newx][newy] = cell
                self.grid[oldX][oldY] = None
                return -1 # plain old move
        return 0



    def immuneSupport(self, cell:HelperImmuneCell):
        # boosts immune cell proliferation and reduces infected
        # cell's infection probability
        localCells = self.getLocalCells(cell.x, cell.y, cell.window)
        if len(localCells) == 0: return 0
        for _cell in localCells:
            if _cell.infected: _cell.boost(1./cell.helper_boost, cell.boost_count)
            elif _cell.immune: _cell.boost(cell.helper_boost, cell.boost_count)
        cell.support = True
        return 1

    def immuneSuppression(self, cell:HelperImmuneCell):
        # boosts healthy cell proliferation
        localCells = self.getLocalCells(cell.x, cell.y, cell.window)
        if len(localCells) == 0: return 0
        for _cell in localCells:
            if not _cell.infected and not _cell.immune: _cell.boost(cell.helper_boost, cell.boost_count)
            elif _cell.immune: _cell.boost(1./(2*cell.helper_boost), cell.boost_count)
        cell.suppress = True
        return 1

    def immuneAttack(self, cell:NaiveImmuneCell):
        neighbors = self.getNeighbors(cell.x, cell.y)
        _succ = deepcopy(cell.attack_success)
        if cell.boosted: _succ = 0.99
        if bernoulli.rvs(_succ) == 1: # NOTE: random probability
            cell.boost(2, 2) # NOTE
            score = 0
            for neighbor in neighbors:
                self.add(neighbor.x,neighbor.y,None)
                self.cells.remove(neighbor) # NOTE: this could be an issue
                score += 1
            return score
        return 0

    def reproduceCell(self, cell):
        #reproduces cell if random number is less than reproduction probability
        neighs = self.getEmptyNeighbors(cell.x, cell.y)
        if len(neighs) > 0:
            newCoords = rand.choice(neighs) # TODO Random
            newCell = cell.reproduce(newCoords[0], newCoords[1])
            if newCell.boosted: newCell.revert()
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
                if not neighbor.infected:
                    if neighbor in self.cells: self.cells.remove(neighbor)
                    neighbor.infected=True
                    self.cells.append(neighbor)
                    self.add(neighbor.x, neighbor.y, neighbor)
                    numInfected += 1
        return numInfected
    

    def die(self, cell):
        #kills cell if random number is less than death probability
        self.grid[cell.x][cell.y] = None
        if cell in self.cells: self.cells.remove(cell) # NOTE: this could be an issue
        return 1
    

    def getLocalArea(self, x, y, radius):
        lowerX = x-radius
        if lowerX < 0: lowerX = 0

        higherX = x+radius
        if higherX >= self.width: higherX = self.width - 1

        lowerY = y-radius
        if lowerY < 0: lowerY = 0

        higherY = y+radius
        if higherY >= self.height: higherY = self.height - 1

        lowerX = int(lowerX)
        lowerY = int(lowerY)
        higherX = int(higherX)
        higherY = int(higherY)

        return lowerX, lowerY, higherX, higherY


    def getLocalCells(self, x, y, radius): 
        # NOTE keep in mind this radius
        # NOTE: removes the given cell from local cells
        lowerX, lowerY, higherX, higherY = self.getLocalArea(x, y, radius)


        subGrid = self.grid[lowerY:higherY+1] # NOTE: +1 for slicing
        subGrid = [row[lowerX:higherX+1] for row in subGrid]
        noNoneCells = [cell for cell in list(chain(*subGrid)) if cell is not None and (cell.x != x or cell.y != y)]
        return noNoneCells


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
    

    def getNeighborPos(self, x, y):
        neighbors = []
        if y+1 < self.height:
            neighbors.append((x, y+1))
        if y-1 >= 0:
            neighbors.append((x, y-1))
        if x+1 < self.width:
            neighbors.append((x-1, y))
        if x-1 >= 0:
            neighbors.append((x+1, y))
        return neighbors
    

    def getAllCellsList(self):
        return self.cells

    def getAllCellsGrid(self):
        #returns list of all Cell objects in grid
        return [cell for cell in list(chain(*self.grid)) if cell is not None]
    

    def __str__(self):
        out = [[str(self.grid[x][y])[0] for x in range(self.width)]
               for y in range(self.height)]
        out = [[s.replace("N", " ") for s in line ] for line in out]
        out.reverse()
        return '\n'.join([''.join(x) for x in out])