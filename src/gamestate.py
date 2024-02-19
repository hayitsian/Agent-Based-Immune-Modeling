
from scipy.stats import bernoulli
from cell import BaseCell, NaiveImmuneCell, SmartImmuneCell, HelperImmuneCell
from agents import NaiveUtility, SmartUtility
from grid import Grid
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
        self.grid = Grid(width, height) # TODO GRID STUFFFFFFFFF

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
        self.grid.loadCells(cells)
        return self
    

    def updateCellParams(self):
        # NOTE: updates the probabilities within cells before performing calculations
        for cell in self.cells:
            lowerX, lowerY, higherX, higherY = self.grid.getLocalArea(cell.x, cell.y, cell.window)
            _localArea = (higherX - lowerX) * (higherY - lowerY)
            _localCells = self.grid.getLocalCells(cell.x, cell.y, cell.window)
            # if not cell.boosted: cell.updateParams(_localCells, _localArea) # NOTE commenting out boosting stuff for now
            cell.decrementCounter()


    def calculateImmuneActivations(self):
        immActs = []

        for cell in self.cells:
            if cell.immune:
                lowerX, lowerY, higherX, higherY = self.grid.getLocalArea(cell.x, cell.y, cell.window)
                _localArea = (higherX - lowerX) * (higherY - lowerY)
                _localCells = self.grid.getLocalCells(cell.x, cell.y, cell.window)
                immActs.append(self.utility(cell, _localCells, _localArea)[0])

            else: immActs.append("PASS")

        return immActs


    def calculateReproductions(self):
        return bernoulli.rvs([cell.repro_prob for cell in self.cells]).tolist()


    def calculateInfections(self):
        return bernoulli.rvs([cell.infection_prob for cell in self.cells]).tolist()


    def calculateDeaths(self):
        return bernoulli.rvs([cell.die_prob for cell in self.cells]).tolist()


    def performImmuneActivations(self, listOfActions: list[str]):
        # for each cell
            # if immune
                # do the immune activation
            # if cell killed
                # remove from list of cells and cell grid
                # pop its index and return it

        deads = []
        
        for _idx, _cell in enumerate(self.cells): # the self.cells should be updated by immuneAct
            assert len(self.cells) == len(listOfActions), f"Number of cells: {len(self.cells)}, Number of immune actions: {len(listOfActions)}"
            if _cell.immune:
                _action = listOfActions[_idx]
                if _action == "ATTACK":
                    # perform the action
                    _res = self.immuneAct(_cell, _action) # returns list of indexes removed (or an empty list, or a list of [-1] if unsuccessful)
                    if len(_res) > 0:
                        for __idx in _res:
                            if __idx > -1:
                                deads.append(__idx)
                                del listOfActions[__idx]
        return deads


    def performApoptosisDeaths(self, listOfDeaths: list[int]):
        # for each cell
            # if dead
                # pop its index and return it

        deads = []

        for _idx, _cell in enumerate(self.cells): # the self.cells should be updated by die
            # these lists are not always the same length (may be removing a cell before its death action?)
            assert len(self.cells) == len(listOfDeaths), f"Number of cells: {len(self.cells)}, Number of death actions: {len(listOfDeaths)}"
            _death = listOfDeaths[_idx]
            if _death == 1:
                # perform the action
                _res = self.die(_cell)
                if _res > -1:
                    deads.append(_res)
                    del listOfDeaths[_res]

        return deads


    def performReproductions(self, listOfRepr: list[int]):
        # for each cell
            # if reproduction
                # pop its index and return it

        newCells = []

        for _idx, _cell in enumerate(self.cells): # the self.cells should be updated by reproduce
            assert len(self.cells) == len(listOfRepr), f"Number of cells: {len(self.cells)}, Number of reproduce actions: {len(listOfRepr)}"
            _repr = listOfRepr[_idx]
            if _repr == 1:
                # perform the action
                _res = self.reproduceCell(_cell)
                if _res > -1:
                    newCells.append(_res)
                    listOfRepr.insert(_res, 0)
        return newCells


    def performInfections(self, listOfInf: list[int]):
        # for each cell
            # if infected
                # update its neighbors
        _res = 0
        for _idx, _cell in enumerate(self.cells): # the self.cells should be updated by infect
            _repr = listOfInf[_idx]
            if _repr == 1:
                # perform the action
                _res += self.infectCell(_cell)
        return _res


    def performMovement(self, listOfActions: list[str]):
        # for each cell
            # if immune
                # do the immune activation

        moves = 0
        
        for _idx, _cell in enumerate(self.cells): # the self.cells should be updated by immuneAct
            assert len(self.cells) == len(listOfActions), f"Number of cells: {len(self.cells)}, Number of movements: {len(listOfActions)}"
            if _cell.immune:
                _action = listOfActions[_idx]
                if _action == "MOVE":
                    # perform the action
                    _res = self.immuneAct(_cell, _action)
                    if _res != 0:
                        moves += 1
        return moves



    def immuneAct(self, cell:NaiveImmuneCell, action:str):
        assert cell.immune, "Trying to perform ImmuneAct on a non-immune cell"
        if cell.helper: cell.suppress = cell.support = False
        if cell.activated: cell.activated = False

        lowerX, lowerY, higherX, higherY = self.grid.getLocalArea(cell.x, cell.y, cell.window)
        localArea = (higherX - lowerX) * (higherY - lowerY)

        if action == "ATTACK": # attack
            cell.activated = True
            if cell.helper: 
                cell.activate(self.grid.getLocalCells(cell.x, cell.y, cell.window), localArea) # TODO i do not like this being calculated in a cell; it should be in an agent or grid
                if cell.suppress: return self.immuneSuppression(cell)
                elif cell.support: return self.immuneSupport(cell)
            return self.immuneAttack(cell)
        
        elif action == "MOVE": # move
            return self.moveCell(cell)
        
        elif action == "PASS": # pass
            return 0
        return 0
    


    def moveCell(self, cell):
        if cell.immune: return self.grid.moveCell(cell, self.endocrineWindow)
        else: return 0


    """
    These immune support, suppression, and activation numbers need to be abstracted out.
    They also need to be looked at carefully as the behavior of the model is inconsistent with what we want.
    """

    def immuneSupport(self, cell:HelperImmuneCell):
        # boosts immune cell proliferation and reduces infected cell's infection probability
        localCells = self.grid.getLocalCells(cell.x, cell.y, cell.window)
        if len(localCells) == 0: return -1
        for _cell in localCells:
            if _cell.infected: _cell.boost(1./cell.helper_boost, cell.boost_count)
            elif _cell.immune: _cell.boost(cell.helper_boost, cell.boost_count)
        cell.support = True
        return [-1]


    def immuneSuppression(self, cell:HelperImmuneCell):
        # boosts healthy cell proliferation
        localCells = self.grid.getLocalCells(cell.x, cell.y, cell.window)
        if len(localCells) == 0: return -1
        for _cell in localCells:
            if not _cell.infected and not _cell.immune: _cell.boost(cell.helper_boost, cell.boost_count)
            elif _cell.immune: _cell.boost(1./(2*cell.helper_boost), cell.boost_count)
        cell.suppress = True
        return [-1]


    def immuneAttack(self, cell:NaiveImmuneCell):
        neighbors = self.grid.getNeighbors(cell.x, cell.y)
        _succ = deepcopy(cell.attack_success)
        if cell.boosted: _succ = 0.99 # NOTE NOTE NOTE
        if bernoulli.rvs(_succ) == 1: # NOTE: random probability
            # cell.boost(2, 2) # NOTE
            score = []
            for neighbor in neighbors:
                neighborIdx = self.cells.index(neighbor)
                self.cells.remove(neighbor) # TODO: this could be an issue
                self.grid.removeCell(neighbor.x, neighbor.y) # NOTE updates the grid
                score.append(neighborIdx)
            return score
        return [-1]


    """
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """


    def reproduceCell(self, cell):
        #reproduces cell if random number is less than reproduction probability
        neighs = self.grid.getEmptyNeighbors(cell.x, cell.y)
        if len(neighs) > 0:
            newCoords = rand.choice(neighs) # NOTE Random
            newCell = cell.reproduce() # gets a deepcopy of this cell
            newCell.x = newCoords[0]
            newCell.y = newCoords[1]
            if newCell.boosted: newCell.revert()
            self.grid.addCell(newCoords[0], newCoords[1], newCell) # updates the grid
            self.cells.append(newCell)
            return self.cells.index(newCell)
        return -1


    def infectCell(self, cell):
        #infects neighbor cells if infected with probability of infection
        numInfected = 0
        if cell.infected:
            neighbors = self.grid.getNeighbors(cell.x, cell.y)
            for neighbor in neighbors:
                if neighbor.immune: continue
                if not neighbor.infected:
                    assert neighbor in self.cells
                    neighbor.infect()
                    numInfected += 1
        return numInfected
    

    def die(self, cell):
        #kills cell if random number is less than death probability
        _idx = -1
        if cell in self.cells:
            _idx = self.cells.index(cell)
            self.cells.remove(cell) # TODO: this could be an issue
            self.grid.removeCell(cell.x, cell.y) # NOTE updates the grid
        return _idx
    

    def getAllCellsList(self):
        return self.cells

    def getAllCellsGrid(self):
        #returns list of all Cell objects in grid
        return self.grid.getAllCells()
    

    def shuffleCells(self):
        # NOTE: IMPORTANT
        rand.shuffle(self.cells)


    def __str__(self):
        return str(self.grid)