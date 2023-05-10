#!/usr/bin/env python3

from gamestate import GameState
from cell import BaseCell, NaiveImmuneCell, HelperImmuneCell
from cellAgents import NaiveUtility
from copy import copy
import numpy as np

def testLocalCells():
    state1 = GameState(width=3, height=3)
    cell1 = BaseCell(1, 1, 1)
    cell2 = BaseCell(0, 0, 1)
    cell3 = BaseCell(1, 0, 1)
    cell4 = BaseCell(2, 2, 1, infected=True)
    cells1 = [cell1,
              cell2,
              cell3,
              cell4]
    
    state1.load(cells1)
    # print(str(state1))

    immLocalCells = state1.getLocalCells(1, 1, 1)
    assert cell2 in immLocalCells, "Cell2 not in local cells"
    assert cell3 in immLocalCells, "Cell3 not in local cells"
    assert cell4 in immLocalCells, "Cell4 not in local cells"
    assert cell1 not in immLocalCells, "Self cell in local cells"


    state2 = GameState(width=5, height=5)
    cell5 = BaseCell(2, 3, 1)
    cell6 = BaseCell(4, 3, 1, infected=True)
    cell7 = BaseCell(3, 3, 1)
    cell8 = BaseCell(1, 3, 1)
    cells2 = copy(cells1)
    cells2.extend([cell5, cell6, cell7, cell8])
              
    state2.load(cells2)
    # print(str(state2))
    baseLocalCells = state2.getLocalCells(2, 2, 1)

    assert cell2 not in baseLocalCells, "Cell2 in local cells"
    assert cell3 not in baseLocalCells, "Cell3 in local cells"
    assert cell4 not in baseLocalCells, "Self cell in local cells"
    assert cell8 in baseLocalCells, "Cell8 not in local cells"
    assert cell1 in baseLocalCells, "Cell1 not in local cells"
    assert cell5 in baseLocalCells, "Cell5 not in local cells"
    assert cell6 not in baseLocalCells, "cell6 in local cells"
    assert cell7 in baseLocalCells, "Cell7 not in local cells"
    

    state3 = GameState(width=5, height=5)
    cell9 = BaseCell(4, 4, 2)
    cell10 = BaseCell(3, 4, 1)

    cells3 = copy(cells2)
    cells3.extend([cell9, cell10])
    
    state3.load(cells3)
    # print(str(state3))

    baseLocalCells = state3.getLocalCells(4, 4, 2)
    assert cell1 not in baseLocalCells, "Cell1 in local cells"
    assert cell2 not in baseLocalCells, "Cell2 in local cells"
    assert cell3 not in baseLocalCells, "Cell3 in local cells"
    assert cell4 in baseLocalCells, "Cell4 not in local cells"
    assert cell7 in baseLocalCells, "Cell7 not in local cells"
    assert cell5 in baseLocalCells, "Cell5 not in local cells"
    assert cell6 in baseLocalCells, "Cell6 not in local cells"
    assert cell9 not in baseLocalCells, "Self cell in local cells"
    assert cell8 not in baseLocalCells, "cell8 in local cells"
    assert cell10 in baseLocalCells, "cell10 not in local cells"



def testNaiveUtility():
    state1 = GameState(width=3, height=3)
    cell1 = NaiveImmuneCell(1, 1, 1, attack_success=1.0)
    cell2 = BaseCell(0, 0, 1)
    cell3 = BaseCell(1, 0, 1, infected=True)
    cell4 = BaseCell(2, 2, 1, infected=True)
    cells1 = [cell1,
              cell2,
              cell3,
              cell4]
    
    state1.load(cells1)
    # print(str(state1))

    immLocalCells = state1.getLocalCells(cell1.x, cell1.y, cell1.window)
    lowerX, lowerY, higherX, higherY = state1.getLocalArea(cell1.x, cell1.y, cell1.window)
    immLocalArea = (higherX - lowerX) * (higherY - lowerY)

    action, utilDict = NaiveUtility(cell1, immLocalCells, immLocalArea)

    assert action=="ATTACK", f"Cell1 does not attack: {action}"
    attackVal = utilDict["ATTACK"]
    assert attackVal==39.5, f"Cell1 attack utility wrong: expected 39.5 received { attackVal }"
    moveVal = utilDict["MOVE"]
    assert moveVal==0.5, f"Cell1 move utility wrong: expected 0.5 received { moveVal }"
    passVal = utilDict["PASS"]
    assert passVal==-np.inf, f"Cell1 pass utility wrong: expected -infinity received { passVal }"



    state2 = GameState(width=3, height=3)
    cell1 = NaiveImmuneCell(1, 1, 1, attack_success=1.0)
    cell2 = BaseCell(0, 1, 1)
    cell3 = BaseCell(1, 0, 1, infected=True)
    cell4 = BaseCell(2, 2, 1, infected=True)
    cell5 = BaseCell(2, 1, 1)
    cells2 = [cell1,
              cell2,
              cell3,
              cell4,
              cell5]
    
    state2.load(cells2)
    # print(str(state2))

    immLocalCells = state2.getLocalCells(cell1.x, cell1.y, cell1.window)
    lowerX, lowerY, higherX, higherY = state2.getLocalArea(cell1.x, cell1.y, cell1.window)
    immLocalArea = (higherX - lowerX) * (higherY - lowerY)

    action, utilDict = NaiveUtility(cell1, immLocalCells, immLocalArea)

    assert action=="ATTACK", f"Cell1 does not attack: {action}"
    attackVal = utilDict["ATTACK"]
    assert attackVal==19.5, f"Cell1 attack utility wrong: expected 19.5 received { attackVal }"
    moveVal = utilDict["MOVE"]
    assert moveVal==0.5, f"Cell1 move utility wrong: expected 0.5 received { moveVal }"
    passVal = utilDict["PASS"]
    assert passVal==-np.inf, f"Cell1 pass utility wrong: expected -infinity received { passVal }"



    state3 = GameState(width=7, height=7)
    cell1 = NaiveImmuneCell(2, 2, 2, attack_success=1.0)
    cell2 = BaseCell(0, 0, 1)
    cell3 = BaseCell(1, 0, 1)
    cell4 = BaseCell(1, 2, 1)
    cell5 = BaseCell(5, 5, 1, infected=True)
    cell6 = BaseCell(5, 6, 1, infected=True)
    cell7 = BaseCell(6, 5, 1, infected=True)
    cells3 = [cell1,
              cell2,
              cell3,
              cell4,
              cell5,
              cell6,
              cell7]
    
    state3.load(cells3)
    # print(str(state3))

    immLocalCells = state3.getLocalCells(cell1.x, cell1.y, cell1.window)
    lowerX, lowerY, higherX, higherY = state3.getLocalArea(cell1.x, cell1.y, cell1.window)
    immLocalArea = (higherX - lowerX) * (higherY - lowerY)

    action, utilDict = NaiveUtility(cell1, immLocalCells, immLocalArea)

    assert action=="MOVE", f"Cell1 does not move: {action}"
    attackVal = utilDict["ATTACK"]
    assert attackVal==-10., f"Cell1 attack utility wrong: expected -10. received { attackVal }"
    moveVal = utilDict["MOVE"]
    assert moveVal==2.5, f"Cell1 move utility wrong: expected 2.5 received { moveVal }"
    passVal = utilDict["PASS"]
    assert passVal==-np.inf, f"Cell1 pass utility wrong: expected -infinity received { passVal }"



    state4 = GameState(width=7, height=7)
    cell1 = NaiveImmuneCell(2, 2, 4, attack_success=1.0)
    cell2 = NaiveImmuneCell(0, 6, 1, attack_success=1.0)
    cell3 = NaiveImmuneCell(1, 6, 1, attack_success=1.0)
    cell4 = NaiveImmuneCell(2, 6, 1, attack_success=1.0)
    cell5 = NaiveImmuneCell(3, 6, 1, attack_success=1.0)
    cell6 = NaiveImmuneCell(4, 6, 1, attack_success=1.0)
    cell7 = NaiveImmuneCell(5, 6, 1, attack_success=1.0)
    cell8 = NaiveImmuneCell(0, 5, 1, attack_success=1.0)
    cell9 = NaiveImmuneCell(1, 3, 1, attack_success=1.0)
    cell10 = NaiveImmuneCell(2, 4, 1, attack_success=1.0)
    cell11 = NaiveImmuneCell(3, 4, 1, attack_success=1.0)
    cell12 = NaiveImmuneCell(4, 5, 1, attack_success=1.0)
    cell13 = NaiveImmuneCell(5, 5, 1, attack_success=1.0)
    cell14 = BaseCell(0, 0, 1, infected=True)
    cell15 = BaseCell(1, 0, 1, infected=True)
    cell16 = BaseCell(1, 2, 1, infected=True)
    cell17 = BaseCell(5, 1, 1, infected=True)
    cell18 = BaseCell(5, 0, 1, infected=True)
    cell19 = BaseCell(6, 0, 1, infected=True)
    cell20 = BaseCell(2, 1, 1, infected=True)
    cell21 = NaiveImmuneCell(2, 3, 1, attack_success=1.0)
    cell22 = NaiveImmuneCell(3, 2, 1, attack_success=1.0)
    cells4 = [cell1,
              cell2,
              cell3,
              cell4,
              cell5,
              cell6,
              cell7,
              cell8,
              cell9,
              cell10,
              cell11,
              cell12,
              cell13,
              cell14,
              cell15,
              cell16,
              cell17,
              cell18,
              cell19,
              cell20,
              cell21,
              cell22]
    
    state4.load(cells4)
    # print(str(state4))

    immLocalCells = state4.getLocalCells(cell1.x, cell1.y, cell1.window)
    lowerX, lowerY, higherX, higherY = state4.getLocalArea(cell1.x, cell1.y, cell1.window)
    immLocalArea = (higherX - lowerX) * (higherY - lowerY)

    action, utilDict = NaiveUtility(cell1, immLocalCells, immLocalArea)

    assert action=="ATTACK", f"Cell1 does not move: {action}"
    attackVal = utilDict["ATTACK"]
    assert attackVal==79.0, f"Cell1 attack utility wrong: expected 79.0 received { attackVal }"
    moveVal = utilDict["MOVE"]
    assert moveVal==0.5, f"Cell1 move utility wrong: expected 0.5 received { moveVal }"
    passVal = utilDict["PASS"]
    assert passVal==-np.inf, f"Cell1 pass utility wrong: expected -infinity received { passVal }"



    state5 = GameState(width=7, height=7)
    cell1 = NaiveImmuneCell(2, 2, 4, attack_success=1.0)
    cell2 = NaiveImmuneCell(0, 6, 1, attack_success=1.0)
    cell3 = NaiveImmuneCell(1, 6, 1, attack_success=1.0)
    cell4 = NaiveImmuneCell(2, 6, 1, attack_success=1.0)
    cell5 = NaiveImmuneCell(3, 6, 4, attack_success=1.0)
    cell6 = NaiveImmuneCell(4, 6, 1, attack_success=1.0)
    cell7 = NaiveImmuneCell(5, 6, 1, attack_success=1.0)
    cell23 = NaiveImmuneCell(6, 6, 2, attack_success=1.0)
    cell8 = NaiveImmuneCell(0, 5, 1, attack_success=1.0)
    cell9 = NaiveImmuneCell(1, 5, 1, attack_success=1.0)
    cell10 = NaiveImmuneCell(2, 5, 1, attack_success=1.0)
    cell11 = NaiveImmuneCell(3, 5, 1, attack_success=1.0)
    cell12 = NaiveImmuneCell(4, 5, 1, attack_success=1.0)
    cell13 = NaiveImmuneCell(5, 5, 1, attack_success=1.0)
    cell24 = NaiveImmuneCell(6, 5, 1, attack_success=1.0)
    cell25 = NaiveImmuneCell(0, 4, 1, attack_success=1.0)
    cell26 = NaiveImmuneCell(1, 4, 1, attack_success=1.0)
    cell27 = NaiveImmuneCell(2, 4, 1, attack_success=1.0)
    cell28 = NaiveImmuneCell(3, 4, 1, attack_success=1.0)
    cell29 = NaiveImmuneCell(4, 4, 1, attack_success=1.0)
    cell30 = NaiveImmuneCell(5, 4, 1, attack_success=1.0)
    cell31 = NaiveImmuneCell(6, 4, 1, attack_success=1.0)
    cell14 = BaseCell(0, 0, 1, infected=True)
    cell15 = BaseCell(1, 0, 1, infected=True)
    cell16 = BaseCell(1, 2, 1, infected=True)
    cell17 = BaseCell(5, 1, 1, infected=True)
    cell18 = BaseCell(5, 0, 1, infected=True)
    cell19 = BaseCell(6, 0, 1, infected=True)
    cell20 = BaseCell(2, 1, 1, infected=True)
    cell21 = NaiveImmuneCell(2, 3, 4, attack_success=1.0)
    cell22 = NaiveImmuneCell(3, 2, 1, attack_success=1.0)
    cell32 = BaseCell(3, 3, 1, infected=True)
    cell33 = BaseCell(1, 3, 1, infected=True)
    cell34 = BaseCell(2, 0, 1, infected=True)
    cell35 = BaseCell(3, 0, 1, infected=True)
    cell36 = BaseCell(4, 0, 1, infected=True)
    cell37 = BaseCell(1, 1, 1, infected=True)
    cell38 = BaseCell(3, 1, 1, infected=True)
    cell39 = BaseCell(4, 1, 1, infected=True)
    cell40 = BaseCell(6, 1, 1, infected=True)
    cell41 = NaiveImmuneCell(0, 1, 1, attack_success=1.0)
    cell42 = NaiveImmuneCell(0, 2, 1, attack_success=1.0)
    cell43 = NaiveImmuneCell(0, 3, 1, attack_success=1.0)
    cell44 = NaiveImmuneCell(4, 2, 1, attack_success=1.0)
    cell45 = NaiveImmuneCell(4, 3, 1, attack_success=1.0)
    cell46 = NaiveImmuneCell(5, 3, 1, attack_success=1.0)
    cells5 = [cell1,
              cell2,
              cell3,
              cell4,
              cell5,
              cell6,
              cell7,
              cell8,
              cell9,
              cell10,
              cell11,
              cell12,
              cell13,
              cell14,
              cell15,
              cell16,
              cell17,
              cell18,
              cell19,
              cell20,
              cell21,
              cell22,
              cell23,
              cell24,
              cell25,
              cell26,
              cell27,
              cell28,
              cell29,
              cell30,
              cell31,
              cell32,
              cell33,
              cell34,
              cell35,
              cell36,
              cell37,
              cell38,
              cell39,
              cell40,
              cell41,
              cell42,
              cell43,
              cell44,
              cell45,
              cell46]
    
    state5.load(cells5)
    # print(str(state5))

    immLocalCells = state5.getLocalCells(cell21.x, cell21.y, cell21.window)
    lowerX, lowerY, higherX, higherY = state5.getLocalArea(cell21.x, cell21.y, cell21.window)
    immLocalArea = (higherX - lowerX) * (higherY - lowerY)

    action, utilDict = NaiveUtility(cell21, immLocalCells, immLocalArea)

    assert action=="ATTACK", f"Cell21 does not attack: {action}"
    attackVal = utilDict["ATTACK"]
    assert attackVal==79.0, f"Cell21 attack utility wrong: expected 79.0 received { attackVal }"
    moveVal = utilDict["MOVE"]
    assert moveVal==0.5, f"Cell21 move utility wrong: expected 0.5 received { moveVal }"
    passVal = utilDict["PASS"]
    assert passVal==-np.inf, f"Cell21 pass utility wrong: expected -infinity received { passVal }"


    immLocalCells = state5.getLocalCells(cell5.x, cell5.y, cell5.window)
    lowerX, lowerY, higherX, higherY = state5.getLocalArea(cell5.x, cell5.y, cell5.window)
    immLocalArea = (higherX - lowerX) * (higherY - lowerY)

    action, utilDict = NaiveUtility(cell5, immLocalCells, immLocalArea)

    assert action=="MOVE", f"Cell5 does not move: {action}"
    attackVal = utilDict["ATTACK"]
    assert attackVal==0.0, f"Cell5 attack utility wrong: expected 0.0 received { attackVal }"
    moveVal = utilDict["MOVE"]
    assert moveVal==0.5, f"Cell5 move utility wrong: expected 0.5 received { moveVal }"
    passVal = utilDict["PASS"]
    assert passVal==-np.inf, f"Cell5 pass utility wrong: expected -infinity received { passVal }"


    immLocalCells = state5.getLocalCells(cell23.x, cell23.y, cell23.window)
    lowerX, lowerY, higherX, higherY = state5.getLocalArea(cell23.x, cell23.y, cell23.window)
    immLocalArea = (higherX - lowerX) * (higherY - lowerY)

    action, utilDict = NaiveUtility(cell23, immLocalCells, immLocalArea)

    assert action=="PASS", f"cell23 does not move: {action}"
    attackVal = utilDict["ATTACK"]
    assert attackVal==0.0, f"cell23 attack utility wrong: expected 0.0 received { attackVal }"
    moveVal = utilDict["MOVE"]
    assert moveVal==0.5, f"cell23 move utility wrong: expected 0.5 received { moveVal }"
    passVal = utilDict["PASS"]
    assert passVal==np.inf, f"cell23 pass utility wrong: expected +infinity received { passVal }"





# TODO: test to make sure game state will not allow cells to overlap
# TODO: test utility functions for immune cells



testLocalCells()
testNaiveUtility()