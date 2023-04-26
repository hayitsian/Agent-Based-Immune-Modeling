#!/usr/bin/env python3

from gamestate import GameState
import random as rand
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer
from cellAgents import NaiveUtility, SmartUtility

def plot(EPOCHS, FIGURE_TITLE, FIGURE_NAME, _labels, data):
    for i in range(len(data)):
        plt.plot(list(range(EPOCHS+1)), data[i], label=_labels[i])

    plt.title(FIGURE_TITLE)
    plt.xlabel("Steps")
    plt.ylabel("# Cells")
    plt.legend()
    plt.savefig(FIGURE_NAME)
    plt.close()


def main(INFECT_PROB = 0.035,
    REPRODUCE_PROB = 0.05,
    DEATH_PROB = 0.03,
    ATTACK_SUCCESS = 0.85,
    IMMUNE_CONSTANT = 1.0,
    HELPER_BOOST = 1.2,
    BOOST_COUNT = 5,
    INIT_CELLS = 50,
    INIT_INFECTED = 8,
    INIT_EFFECTOR = 8,
    INIT_HELPER = 8,
    AUTOCRINE_WINDOW = 3,
    PARACRINE_WINDOW = 8,
    ENDOCRINE_WINDOW = 12,
    WIDTH = 50,
    HEIGHT = 50,
    EPOCHS = 2500,
    PLOT = True,
    VERBOSE = True
    ):

    INIT_IMMUNE = INIT_EFFECTOR + INIT_HELPER
    INIT_HEALTHY = INIT_CELLS - INIT_IMMUNE - INIT_HELPER - INIT_INFECTED


    game = GameState(WIDTH, HEIGHT, utility=NaiveUtility,
                     autocrineWindow = AUTOCRINE_WINDOW, paracrineWindow = PARACRINE_WINDOW,
                     endocrineWindow = ENDOCRINE_WINDOW)

    game.start(INFECT_PROB, REPRODUCE_PROB, DEATH_PROB, 
                 attack_success=ATTACK_SUCCESS, numCells=INIT_CELLS, 
                 numInfected=INIT_INFECTED, numImmune=INIT_EFFECTOR,
                 numHelper = INIT_HELPER, immune_constant=IMMUNE_CONSTANT,
                 helper_boost=HELPER_BOOST, boost_count=BOOST_COUNT)

    if VERBOSE: print("Initial Conditions:" + "\n" + "Number of healthy Cells: " + str(INIT_HEALTHY) + "\n" + "Number of infected Cells: " 
                      + str(INIT_INFECTED) + "\n" + "Number of immune Cells: " + str(INIT_IMMUNE) + "\n")
    if VERBOSE: print("Grid size: " + str(game.width) + "x" + str(game.height) + "\n")
    if VERBOSE: print(str(game) + "\n", end='\r')

    
    labelsCount = ["Epoch", "Cell count", "Healthy cell count", "Infected cell count", "Immune cell count", "Effector immune cell count", "Helper immune cell count"]
    labelsAction = ["Activated cell count", "Reproduced cell count", "Moved cell count", "Infected cell count", "Died cell count", "Killed cell count", "Boosted cell count", "Suppressed cell count"]
    labels = labelsCount+labelsAction

    dataDict = {}
    for _label in labels: 
        dataDict[_label] = []

    dataDict["Epoch"].append(0)
    dataDict["Cell count"].append(INIT_CELLS)
    dataDict["Healthy cell count"].append(INIT_HEALTHY)
    dataDict["Infected cell count"].append(INIT_INFECTED)
    dataDict["Immune cell count"].append(INIT_IMMUNE)
    dataDict["Helper immune cell count"].append(INIT_HELPER)
    dataDict["Effector immune cell count"].append(INIT_EFFECTOR)


    for _label in labelsAction:
        dataDict[_label].append(0)


    startTime = default_timer()

    numSteps = 0

    while numSteps < EPOCHS:

        numSteps += 1

        data = game.step()
        data.insert(0, numSteps)
        dataCount = data[:len(labelsCount)]
        dataAction = data[len(labelsCount):]

        for label, _data in zip(labels, data):
            if VERBOSE: print(f"{label}: {_data}")

        if VERBOSE: print(str(game) + "\n", end='\r')

        for label, _data in zip(labels, data):
            dataDict[label].append(_data)



    time = default_timer() - startTime
    if VERBOSE: print(f"Simulation took: {time}")


    FIGURE_TITLE = f"Cell counts over {EPOCHS} steps {WIDTH}x{HEIGHT} grid\nInfectProb: {INFECT_PROB} ReproProb: {REPRODUCE_PROB} DeathProb: {DEATH_PROB} AttackSuccess: {ATTACK_SUCCESS}\nWith smartUtility immune cell movement"
    FIGURE_NAME = FIGURE_TITLE.replace("\n", " ") + ".png"

    if PLOT: plot(EPOCHS, FIGURE_TITLE, FIGURE_NAME, labelsCount, dataDict[labelsCount].values)

    FIGURE_TITLE = f"Cell actions over {EPOCHS} steps {WIDTH}x{HEIGHT} grid\nInfectProb: {INFECT_PROB} ReproProb: {REPRODUCE_PROB} DeathProb: {DEATH_PROB} AttackSuccess: {ATTACK_SUCCESS}\nWith smartUtility immune cell movement"
    FIGURE_NAME = FIGURE_TITLE.replace("\n", " ") + ".png"

    if PLOT: plot(EPOCHS, FIGURE_TITLE, FIGURE_NAME, labelsAction, dataDict[labelsAction].values)


    return dataDict.values(), labels, len(labelsCount)

main()