

from gamestate import GameState
from agents import NaiveUtility
from cell import BaseCell, SmartImmuneCell, HelperImmuneCell
import random
from scipy.stats import bernoulli
import util

class Game():


    def __init__():
        pass


    def simpleRandomInitialization(width, height, infection_prob, repro_prob, die_prob, 
                                   immune_constant=0.75, attack_success=.75, 
                                   helper_boost=1.25, boost_count=5, 
                                   numCells=200, numInfected=20, numEffector=20, numHelper=10,
                                   autocrineWindow = 1, paracrineWindow = 4, endocrineWindow = 8) -> list[BaseCell]:
        cellList = []
        posList = []

        numHealthy = numCells - numInfected - numEffector - numHelper

        i = 0

        while i < numHealthy:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)

            if (x, y) not in posList:
                cell = BaseCell(x, y, window=endocrineWindow, repro=repro_prob, die=die_prob, infec=infection_prob)
                cellList.append(cell)
                posList.append((x, y))
                i += 1

        i = 0
        while i < numInfected:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)

            if (x, y) not in posList:
                cell = BaseCell(x, y, window=endocrineWindow, repro=repro_prob, die=die_prob, infec=infection_prob, infected=True)
                cellList.append(cell)
                posList.append((x, y))
                i += 1

        i = 0
        while i < numEffector:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)

            if (x, y) not in posList:
                cell = SmartImmuneCell(x, y, window=autocrineWindow, attack_success=attack_success, immune_constant=immune_constant, repro=0.0, die=0.0) # NOTE changed the repro and die probs to 0 for testing
                cellList.append(cell)
                posList.append((x, y))
                i += 1

        i = 0
        while i < numHelper:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)

            if (x, y) not in posList:
                cell = HelperImmuneCell(x, y, window=paracrineWindow, helper_boost=helper_boost, boost_count=boost_count, immune_constant=immune_constant, repro=repro_prob, die=die_prob)
                cellList.append(cell)
                posList.append((x, y))
                i += 1

        assert len(cellList) == numCells, f"Number of cells created: {len(cellList)} number of cells desired: {numCells}"

        """
        if len(cellList) != numCells: return Game.simpleRandomInitialization(width=width, height=height, 
                                                infection_prob=infection_prob, repro_prob=repro_prob, die_prob=die_prob,
                                                immune_constant=immune_constant, attack_success=attack_success,
                                                helper_boost=helper_boost, boost_count=boost_count,
                                                numCells=numCells, numInfected=numInfected, numEffector=numEffector, numHelper=numHelper,
                                                autocrineWindow=autocrineWindow, paracrineWindow=paracrineWindow, endocrineWindow=endocrineWindow)
        """
        
        return cellList



    def simpleStepping(gameState: GameState):

        # NOTE: perform action calculations (in gameState)
        gameState.shuffleCells()
        gameState.updateCellParams()
        actionList = gameState.calculateImmuneActivations()
        reprList = gameState.calculateReproductions()
        infList = gameState.calculateInfections()
        dieList = gameState.calculateDeaths()

        # calculate action data
        _numActivated = actionList.count("ATTACK")
        _numMoved = actionList.count("MOVE")
        _numInfected = infList.count(1)
        _numReproduce = reprList.count(1)
        _numKilled = 0 # immune attacks
        _numDied = 0
        
        # TODO update these lists so that any died cells cannot reproduce move attack or infect others

        # NOTE: priority
        # immune activation > apoptosis > reproduction > infection > movement
        
        # NOTE: perform the actions and get data

        # TODO: not a fan of all this list updating happening here; move everything to GameState

        # immune activation (no moving)
        _deadCells = gameState.performImmuneActivations(actionList)
        reprList = util.removeIndexesFromList(reprList, _deadCells)
        infList = util.removeIndexesFromList(infList, _deadCells)
        dieList = util.removeIndexesFromList(dieList, _deadCells)
        _numKilled = len(_deadCells)

        # apoptosis
        _deadCells = gameState.performApoptosisDeaths(dieList)
        reprList = util.removeIndexesFromList(reprList, _deadCells)
        infList = util.removeIndexesFromList(infList, _deadCells)
        actionList = util.removeIndexesFromList(actionList, _deadCells)
        _numDied += len(_deadCells)

        # reproduction
        _newCells = gameState.performReproductions(reprList)
        dieList = util.addItemAtIndexesToList(dieList, _newCells, 0)
        infList = util.addItemAtIndexesToList(infList, _newCells, 0)
        actionList = util.addItemAtIndexesToList(actionList, _newCells, "PASS")
        
        # infection
        _numInfected = gameState.performInfections(infList)

        # movement
        _numMoved = gameState.performMovement(actionList)


        # calculate more data to ouput
        numCells = len(gameState.getAllCellsList())
        numInfected = sum([cell.infected for cell in gameState.getAllCellsList()])
        numImmune = sum([cell.immune for cell in gameState.getAllCellsList()])
        numHelper = sum([cell.helper for cell in gameState.getAllCellsList()])
        numHealthy = numCells - numImmune - numInfected
        numEffector = numImmune - numHelper

        assert len(gameState.getAllCellsList()) == len(gameState.getAllCellsGrid()), f"Number of gameState cells: {len(gameState.getAllCellsList())}    Number of Grid cells: {len(gameState.getAllCellsGrid())}"

        return gameState, [numCells, numHealthy, numInfected, numImmune, numEffector, numHelper, _numReproduce, _numMoved, _numInfected, _numDied, _numActivated, _numKilled]






    def start(width=100, height=100,
                utility = NaiveUtility, autocrineWindow = 1,
                paracrineWindow = 4, endocrineWindow = 8,
                infection_prob = 0.035, repro_prob = 0.05, 
                die_prob = 0.03, immune_constant=0.75, attack_success=.75, 
                helper_boost=1.25, boost_count=5, numCells=200, 
                numInfected=20, numEffector=20, numHelper=10) -> GameState:

        gameState = GameState(width, height, utility, autocrineWindow, paracrineWindow, endocrineWindow)

        cells = Game.simpleRandomInitialization(width=width, height=height, 
                                                infection_prob=infection_prob, repro_prob=repro_prob, die_prob=die_prob,
                                                immune_constant=immune_constant, attack_success=attack_success,
                                                helper_boost=helper_boost, boost_count=boost_count,
                                                numCells=numCells, numInfected=numInfected, numEffector=numEffector, numHelper=numHelper,
                                                autocrineWindow=autocrineWindow, paracrineWindow=paracrineWindow, endocrineWindow=endocrineWindow)

        gameState = gameState.load(cells)

        return gameState
    



    def step(gameState: GameState):

        gameState, metrics = Game.simpleStepping(gameState)

        return gameState, metrics