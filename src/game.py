

from gamestate import GameState
from cellAgents import NaiveUtility
from cell import BaseCell, SmartImmuneCell, HelperImmuneCell
import random
from scipy.stats import bernoulli

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

        for i in range(numHealthy):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)

            if (x, y) not in posList:
                cell = BaseCell(x, y, window=endocrineWindow, repro=repro_prob, die=die_prob, infec=infection_prob)
                cellList.append(cell)
                posList.append((x, y))
            else: i -= 1

        for i in range(numInfected):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)

            if (x, y) not in posList:
                cell = BaseCell(x, y, window=endocrineWindow, repro=repro_prob, die=die_prob, infec=infection_prob, infected=True)
                cellList.append(cell)
                posList.append((x, y))
            else: i -= 1

        for i in range(numEffector):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)

            if (x, y) not in posList:
                cell = SmartImmuneCell(x, y, window=endocrineWindow, attack_success=attack_success, immune_constant=immune_constant, repro=repro_prob, die=die_prob)
                cellList.append(cell)
                posList.append((x, y))
            else: i -= 1

        for i in range(numHelper):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)

            if (x, y) not in posList:
                cell = HelperImmuneCell(x, y, window=paracrineWindow, helper_boost=helper_boost, boost_count=boost_count, immune_constant=immune_constant, repro=repro_prob, die=die_prob)
                cellList.append(cell)
                posList.append((x, y))
            else: i -= 1

        # assert len(cellList) == numCells, f"Number of cells created: {len(cellList)} number of cells desired: {numCells}"
        # TODO fix this bug
        if len(cellList) != numCells: return Game.simpleRandomInitialization(width=width, height=height, 
                                                infection_prob=infection_prob, repro_prob=repro_prob, die_prob=die_prob,
                                                immune_constant=immune_constant, attack_success=attack_success,
                                                helper_boost=helper_boost, boost_count=boost_count,
                                                numCells=numCells, numInfected=numInfected, numEffector=numEffector, numHelper=numHelper,
                                                autocrineWindow=autocrineWindow, paracrineWindow=paracrineWindow, endocrineWindow=endocrineWindow)
        return cellList



    def simpleStepping(gameState: GameState):
        cells = gameState.getAllCellsList()

        _numActivated = 0
        _numMoved = 0
        _numInfected = 0
        _numReproduce = 0
        _numBoosted = 0 # helper boosts
        _numSuppressed = 0 # helper supresses
        _numKilled = 0 # immune attacks
        _numDied = 0

        random.shuffle(cells)

        localArea = []
        localCells = []
        
        for cell in cells:

            lowerX, lowerY, higherX, higherY = gameState.getLocalArea(cell.x, cell.y, cell.window)
            _localArea = (higherX - lowerX) * (higherY - lowerY)
            _localCells = gameState.getLocalCells(cell.x, cell.y, cell.window)

            localArea.append(_localArea)
            localCells.append(_localCells)

            if not cell.boosted: cell.updateParams(_localCells, _localArea)
            
            cell.decrementCounter()

        actionList = [NaiveUtility(cells[i], localCells[i], localArea[i])[0] for i in range(len(cells)) if cells[i].immune] # only for immune cells
        reprList = bernoulli.rvs([cell.repro_prob for cell in cells])
        infList = bernoulli.rvs([cell.infection_prob for cell in cells])
        dieList = bernoulli.rvs([cell.die_prob for cell in cells])

        immIdx = 0
        # TODO: fix this
        for i in range(len(cells)):

            resAction = 0
            if cells[i].immune: 
                resAction = gameState.immuneAct(cells[i], actionList[immIdx])
                immIdx += 1

            if resAction>0:
                _numActivated += 1
                if cell.helper:
                    if cell.support: _numBoosted += resAction
                    elif cell.suppress: _numSuppressed += resAction
                elif cell.immune: _numKilled += resAction
            elif resAction<0: _numMoved += 1

            resRepr = 0
            if reprList[i]: resRepr = gameState.reproduceCell(cell)
            _numReproduce += resRepr

            resInf = 0
            if infList[i]: resInf = gameState.infectCell(cell)
            _numInfected += resInf

            resDie = 0
            if dieList[i]: resDie = gameState.die(cell)
            _numDied += resDie

            numCellsList = len(gameState.getAllCellsList())
            numCellsGrid = len(gameState.getAllCellsGrid())
            assert numCellsList == numCellsGrid, f"Cells List {numCellsList}, cells grid {numCellsGrid}, action? {resAction} reproduce? {resRepr}, infected? {resInf}, died? {resDie}"

        numCells = len(gameState.getAllCellsList())
        numInfected = sum([cell.infected for cell in gameState.getAllCellsList()])
        numImmune = sum([cell.immune for cell in gameState.getAllCellsList()])
        numHelper = sum([cell.helper for cell in gameState.getAllCellsList()])
        numHealthy = numCells - numImmune - numInfected
        numEffector = numImmune - numHelper

        return gameState, [numCells, numHealthy, numInfected, numImmune, numEffector, numHelper, _numReproduce, _numMoved, _numInfected, _numDied, _numActivated, _numKilled, _numBoosted, _numSuppressed]






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